# Tarea 1 de sistemas distribuidos

**[README de la Tarea 1](https://github.com/cebasttian/SDT12023-2/blob/Felipe/t1/README.md)**:
   - Se describe un "Servidor casero de caché" con nodos Maestro y Esclavo.
   - **Nodo Maestro**: Es el punto de entrada principal para las solicitudes y determina a qué nodo esclavo se debe reenviar una solicitud específica.
   - **Nodo Esclavo**: Almacena datos en caché y responde a las solicitudes según las indicaciones del nodo maestro.
   - Se utiliza **gRPC** para la comunicación entre nodos y **uhashring** para el hashing consistente.
   - Se emplea un algoritmo LRU para gestionar el almacenamiento en caché en cada nodo esclavo.
   - Se describe un "Buscador" que interactúa directamente con el servidor de caché para realizar operaciones. Utiliza gRPC y un archivo JSON como fuente de datos principal.
   - Se proporciona un mini diagrama y pasos sobre cómo levantar el servidor.

**[Código del Servidor](https://github.com/cebasttian/SDT12023-2/blob/Felipe/t1/cache%20server/server.py)**:
   - Implementa un sistema de caché distribuido basado en gRPC.
   - Utiliza un anillo de hash (uhashring) para determinar a qué nodo pertenece una clave específica.
   - El sistema tiene nodos maestros y esclavos. El nodo maestro es responsable de registrar, desregistrar y reenviar solicitudes a nodos esclavos, mientras que los nodos esclavos gestionan las operaciones del caché.

**[Código del Buscador](https://github.com/cebasttian/SDT12023-2/blob/Felipe/t1/search/search.py)**:
   - Representa un cliente que interactúa con el servidor de caché.
   - Permite realizar operaciones de caché como insertar, obtener y eliminar pares clave-valor.
   - Si un valor no se encuentra en el caché, se simula una demora y luego busca la información en un archivo JSON.

**[Definición del Protocolo (Protobuf)](https://github.com/cebasttian/SDT12023-2/blob/Felipe/t1/cache%20server/protos/cache_service.proto)**:
   - Define el servicio `CacheService` con operaciones como `RegisterNode`, `DeregisterNode`, `Get`, `Put` y `Remove`.
   - Define mensajes como `Key`, `CacheItem`, `NodeInfo` y `Response`.

**[Dockerfile](https://github.com/cebasttian/SDT12023-2/blob/Felipe/t1/cache%20server/Dockerfile)**:
   - Se basa en una imagen de Python 3.8.
   - Establece un directorio de trabajo y copia el código fuente al contenedor.
   - Instala las dependencias del proyecto y expone los puertos necesarios.
   - Define un comando para ejecutar la aplicación cuando se inicie el contenedor.


**[Instrucciones]**:


/json 
```
docker compose up --build -d
```
```
docker-compose exec python-app python busqueda_json.py
```

/casero
```
docker compose up -d
```
```
docker exec -it search bash
```
```
python3 search.py
```

/memcached
```
docker-compose up -d
```
```
docker-compose exec python-app python busqueda_memcache.py
```
