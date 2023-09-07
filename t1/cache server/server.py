"""
El código anterior representa una implementación de un sistema de caché distribuido basado en gRPC. 
Utiliza un anillo de hash (uhashring) para determinar a qué nodo pertenece una clave específica. 
El sistema tiene nodos maestros y esclavos. El nodo maestro es responsable de registrar, desregistrar
y reenviar solicitudes a nodos esclavos, mientras que los nodos esclavos se encargan de gestionar las
operaciones del caché.
"""
import grpc
from concurrent import futures
from collections import OrderedDict
import uhashring
import cache_service_pb2_grpc
from cache_service_pb2 import Key, CacheItem, NodeInfo, Response
import argparse

class CacheServiceServicer(cache_service_pb2_grpc.CacheServiceServicer):
    def __init__(self, is_master=True, max_items=100):
        # Indica si el nodo es maestro o no
        self.is_master = is_master
        # Lista que contiene los nodos registrados
        self.nodes = []
        # Anillo de hash utilizado para distribuir las claves entre los nodos
        self.ring = uhashring.HashRing()
        # Cache que almacena pares clave-valor como un diccionario ordenado
        self.cache = OrderedDict()
        # Número máximo de items que puede almacenar el cache
        self.max_items = max_items

    # Función para registrar un nuevo nodo
    def RegisterNode(self, request, context):
        if not self.is_master:
            return Response(success=False, message="Not a master node")
        
        node = f"{request.ip}:{request.port}"
        self.nodes.append(node)
        self.ring.add_node(node)
        
        return Response(success=True, message=f"Node registered successfully")

    # Función para desregistrar un nodo
    def DeregisterNode(self, request, context):
        if not self.is_master:
            return Response(success=False, message="Not a master node")

        node = f"{request.ip}:{request.port}"
        if node in self.nodes:
            self.nodes.remove(node)
            self.ring.remove_node(node)
            return Response(success=True, message="Node deregistered successfully")
        return Response(success=False, message="Node not found")

    # Función para obtener un valor por su clave del cache
    def Get(self, request, context):
        if self.is_master:
            node = self.ring.get_node(request.key)
            print(f"Forwarding retrieval of key '{request.key}' to node: {node}")
            response = forward_request_to_slave(self, node, "Get", request)
            return response
        else:
            value = self.cache.get(request.key, None)
            print(f"Retrieving key '{request.key}:{value}' from local cache")
            if value:
                self.cache.move_to_end(request.key)
                return CacheItem(key=request.key, value=value)
            else:
                return CacheItem(key=request.key, value="")

    # Función para insertar un nuevo par clave-valor en el cache
    def Put(self, request, context):
        if self.is_master:
            all_nodes = self.ring.get_nodes()
            node = self.ring.get_node(request.key)
            print(f"Forwarding insertion of key '{request.key}' to node: {node}")
            print(f"All possible nodes: {all_nodes}")
            response = forward_request_to_slave(self, node, "Put", request)
            return response
        else:
            print(f"Inserting key '{request.key}' in local cache")
            if len(self.cache) >= self.max_items:
                self.cache.popitem(last=False)
            self.cache[request.key] = request.value
            return Response(success=True, message="Inserted successfully")

    # Función para remover un par clave-valor del cache
    def Remove(self, request, context):
        if self.is_master:
            node = self.ring.get_node(request.key)
            print(f"Forwarding retrieval of key '{request.key}' to node: {node}")
            response = forward_request_to_slave(self, node, "Remove", request)
            return response
        else:
            if request.key in self.cache:
                del self.cache[request.key]
                return Response(success=True, message="Removed successfully")
            return Response(success=False, message="Key not found")

# Función para iniciar el servidor gRPC
def serve(is_master=True, port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cache_service_pb2_grpc.add_CacheServiceServicer_to_server(CacheServiceServicer(is_master=is_master), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    if is_master:
        print (f"Master server started on port {port}")
    else:
        print (f"Slave server started on port {port}")
    server.wait_for_termination()

# Función para reenviar una solicitud al nodo esclavo
def forward_request_to_slave(servicer_instance, node, method, *args):
    try:
        with grpc.insecure_channel(node) as channel:
            stub = cache_service_pb2_grpc.CacheServiceStub(channel)
            if method == "Get":
                return stub.Get(*args)
            elif method == "Put":
                return stub.Put(*args)
            elif method == "Remove":
                return stub.Remove(*args)
            else:
                print(f"Unknown method '{method}' requested.")
                return None  # Consider using a default response indicating method error
    except grpc.RpcError as e:
        print(f"RPC error communicating with node {node}. Status: {e.code()}. Details: {e.details()}.")
        # If it's a connection error, consider deregistering the node
        if e.code() == grpc.StatusCode.UNAVAILABLE:
            print(f"Deregistering node {node} due to communication error.")
            ip, port = node.split(":")
            deregister_request = NodeInfo(ip=ip, port=port)
            servicer_instance.DeregisterNode(deregister_request, None)
        return None
    except Exception as e:
        print(f"Unexpected error communicating with node {node}: {e}")
        return None
        
# Función para registrar un nodo esclavo con el nodo maestro
def register_with_master(master_node, slave_ip, slave_port):
    print (f"Registering with master node {master_node}")
    with grpc.insecure_channel(master_node) as channel:
        stub = cache_service_pb2_grpc.CacheServiceStub(channel)
        response = stub.RegisterNode(NodeInfo(ip=slave_ip, port=slave_port))
        print(response.message)

# Punto de entrada del programa
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Distributed Cache Server")
    parser.add_argument("node_type", choices=["master", "slave"], help="Type of the node ('master' or 'slave')")
    parser.add_argument("port", default=50051, type=int, help="Port number to start the node on")
    parser.add_argument("--master_ip", default="localhost", help="IP address of the master node (required if node_type is 'slave')")
    parser.add_argument("--master_port", type=int, default=50051, help="Port number of the master node (required if node_type is 'slave')")
    
    args = parser.parse_args()

    if args.node_type == "master":
        serve(is_master=True, port=args.port)
    elif args.node_type == "slave":
        register_with_master(f"{args.master_ip}:{args.master_port}", "localhost", args.port)
        serve(is_master=False, port=args.port)
    else:
        print("Unknown node type. Use 'master' or 'slave'.")
