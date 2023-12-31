"""
Importaciones: Se importan bibliotecas específicas necesarias para trabajar con 
Protocol Buffers en Python.
_sym_db: Una instancia de la base de datos de símbolos. Es una colección centralizada
de mensajes y servicios de Protocol Buffers.
DESCRIPTOR: Contiene una representación serializada del archivo .proto. Es utilizado
por Protocol Buffers para entender cómo se deben serializar y deserializar los mensajes.
_builder...: Estas líneas generan las clases y funciones de Python basadas en el archivo
.proto original.
if _descriptor...: Esto es para manejar cómo se serializan y deserializan los mensajes,
ya sea utilizando la implementación de C o la implementación de Python."""
# -*- coding: utf-8 -*-
# Indica la codificación del archivo. Es una convención en Python para especificar la codificación UTF-8.

# Generated by the protocol buffer compiler.  DO NOT EDIT!
# Esto nos informa que este archivo ha sido generado automáticamente y no debe ser modificado manualmente.

# source: cache_service.proto
# Indica el archivo de origen que fue utilizado para generar este código.

# Importaciones requeridas para trabajar con Protocol Buffers y gRPC.
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

# Inicialización del símbolo de la base de datos. Se utiliza para registrar y buscar mensajes y servicios de protobuf.
_sym_db = _symbol_database.Default()

# Esta variable almacena una descripción serializada del archivo .proto original.
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'...')

# Esta parte del código crea descriptores para los mensajes y enumera los definidos en el archivo .proto.
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cache_service_pb2', _globals)

# Una verificación para determinar si se deben usar descriptores en C o no.
if _descriptor._USE_C_DESCRIPTORS == False:
    # Configura las opciones de descriptor y los índices de inicio y finalización para cada mensaje serializado.
    DESCRIPTOR._options = None
    _globals['_KEY']._serialized_start=23
    _globals['_KEY']._serialized_end=41
    _globals['_CACHEITEM']._serialized_start=43
    _globals['_CACHEITEM']._serialized_end=82
    _globals['_NODEINFO']._serialized_start=84
    _globals['_NODEINFO']._serialized_end=120
    _globals['_RESPONSE']._serialized_start=122
    _globals['_RESPONSE']._serialized_end=166
    _globals['_CACHESERVICE']._serialized_start=169
    _globals['_CACHESERVICE']._serialized_end=343
# @@protoc_insertion_point(module_scope)
