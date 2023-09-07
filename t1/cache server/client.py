""" 
En resumen, este código representa un cliente simple para un servicio de caché distribuido
que te permite realizar operaciones básicas de caché como insertar (put), obtener (get) y
eliminar (remove) pares clave-valor. Cuando se ejecuta este script, intentará obtener un
valor del caché usando una clave que se pasa como argumento al script.
"""
# Importamos las bibliotecas necesarias. `grpc` es la biblioteca principal para utilizar gRPC en Python.
# Las otras dos importaciones son los archivos generados por el compilador gRPC a partir de la definición del servicio en el archivo `.proto`.
import grpc
import cache_service_pb2
import cache_service_pb2_grpc

# Definimos la clase `CacheClient`, que representa el cliente del servicio de caché.
class CacheClient:
    def __init__(self, host="localhost", port=50051):
        # Establece una conexión (canal) con el servidor gRPC, en este caso, por defecto se conecta a "localhost" en el puerto 50051.
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        # Crea un "stub" que es la representación del cliente para el servicio definido en el archivo `.proto`.
        # Utilizaremos este stub para llamar a los métodos del servicio.
        self.stub = cache_service_pb2_grpc.CacheServiceStub(self.channel)

    # Función para insertar un par clave-valor en el caché.
    def put(self, key, value):
        response = self.stub.Put(cache_service_pb2.CacheItem(key=key, value=value))
        print(response.message)

    # Función para obtener un valor por su clave del caché.
    def get(self, key):
        response = self.stub.Get(cache_service_pb2.Key(key=key))
        # Comprueba si la respuesta tiene un valor asociado. Si es así, lo devuelve.
        if response.value:
            return response.value
        else:
            print("Key not found.")
            return None

    # Función para eliminar un par clave-valor del caché usando una clave dada.
    def remove(self, key):
        response = self.stub.Remove(cache_service_pb2.Key(key=key))
        print(response.message)

# Punto de entrada del programa.
if __name__ == "__main__":
    # Obtiene la clave del primer argumento pasado al script.
    import sys
    key = sys.argv[1]

    # Crea una instancia del cliente.
    client = CacheClient()
    # Utiliza el cliente para obtener un valor del caché usando la clave proporcionada.
    value = client.get(key)
    # Imprime el valor recuperado.
    print(f"Value: {value}")
