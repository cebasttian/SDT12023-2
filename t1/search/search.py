import grpc
import json
import time
import numpy as np
import cache_service_pb2
import cache_service_pb2_grpc

class CacheClient:
    def __init__(self, host="localhost", port=50051, json_file="data.json"):
        # Establecer la conexión con el servidor gRPC
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = cache_service_pb2_grpc.CacheServiceStub(self.channel)
        
        # Cargar el archivo JSON como fuente de datos fallback
        with open(json_file, "r") as file:
            self.data = json.load(file)

    def get(self, key, simulated=False):
        # Registra el tiempo de inicio para calcular el tiempo total de operación
        start_time = time.time()

        # Busca la llave en el caché
        response = self.stub.Get(cache_service_pb2.Key(key=key))
        
        # Si la respuesta contiene un valor, se encontró en el caché
        if response.value:
            elapsed_time = time.time() - start_time
            print(f"Time taken (cache): {elapsed_time:.5f} seconds")
            return response.value
        else:
            # Si no se encuentra, simula una demora (para simular una base de datos lenta, por ejemplo)
            delay = np.random.normal(2, 0.5)
            print(f"Key not found in cache. Waiting {delay:.5f} seconds...")

            if not simulated:
                time.sleep(delay)

            # Si no está en el caché, intenta buscar en el JSON
            value = self.data.get(key, None)
            if value:
                print("Key found in JSON. Adding to cache...")
                
                # Agrega la llave y el valor al caché para futuras búsquedas
                self.stub.Put(cache_service_pb2.CacheItem(key=key, value=value))
                
                elapsed_time = time.time() - start_time
                if simulated:
                    elapsed_time += delay
                print(f"Time taken (JSON + delay): {elapsed_time:.5f} seconds")
                
                return value
            else:
                # No se encontró en el caché ni en el JSON
                elapsed_time = time.time() - start_time
                print(f"Time taken: {elapsed_time:.5f} seconds")
                print("Key not found.")
                return None
            
    def simulate_searches(self, n_searches=10000000):
        # Simula un número de búsquedas con llaves aleatorias
        keys_to_search = [f"key_{i}" for i in np.random.randint(1, 1000001, n_searches)]

        # Métricas iniciales para evaluar el rendimiento del caché
        time_without_cache = 0
        time_with_cache = 0
        avoided_json_lookups = 0

        count = 0
        for key in keys_to_search:
            count += 1
            # Limpia la consola
            print("\033[H\033[J")
            print(f"Searching : {count}/{n_searches}")
            start_time = time.time()
            time_without_cache += 3 + 0.001  # Estimado de tiempo de búsqueda en JSON
            self.get(key)
            elapsed_time = time.time() - start_time
            time_with_cache += elapsed_time

            # Si la búsqueda fue rápida, probablemente fue gracias al caché
            if elapsed_time < 1:
                avoided_json_lookups += 1

        # Resultados finales
        time_saved = time_without_cache - time_with_cache
        print(f"\nTime saved thanks to cache: {time_saved:.2f} seconds")
        print(f"Number of times JSON lookup was avoided: {avoided_json_lookups}")

if __name__ == '__main__':
    # Crea una instancia del cliente y ofrece un menú interactivo al usuario
    client = CacheClient()

    while True:
        print("\nChoose an operation:")
        print("1. Get")
        print("2. Simulate Searches")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            key = input("Enter key: ")
            value = client.get(key)
            if value is not None:
                print(f"Value: {value}")
        elif choice == "2":
            n_searches = int(input("Enter the number of searches you want to simulate: "))
            client.simulate_searches(n_searches)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
