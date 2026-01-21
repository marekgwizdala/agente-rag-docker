import requests
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

# --- CONFIGURACIÓN ---
EMBEDDING_API_URL = "http://127.0.0.1:8080/embed"
QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_NAME = "conocimiento_base"

print("🏗️ Inicializando conexión con Qdrant...")
client = QdrantClient(url=QDRANT_URL)

# 1. Crear la colección
if not client.collection_exists(collection_name=COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    print(f"✅ Colección '{COLLECTION_NAME}' creada.")
else:
    print(f"ℹ️ La colección '{COLLECTION_NAME}' ya existe.")

# 2. Datos
documentos = [
    {"id": 1, "text": "Oracle Cloud Infrastructure ofrece servicios de computación en la nube."},
    {"id": 2, "text": "Python es un lenguaje excelente para Inteligencia Artificial y Backend."},
    {"id": 3, "text": "Docker permite empaquetar aplicaciones en contenedores portátiles."},
    {"id": 4, "text": "La pizza hawaiana genera debates controversiales en la sociedad."},
    {"id": 5, "text": "AWS Lambda es un servicio de computación serverless."}
]

# 3. ETL
print("\n🚀 Iniciando Ingesta de Datos...")
for doc in documentos:
    print(f"Processing doc {doc['id']}...", end=" ")
    try:
        resp = requests.post(EMBEDDING_API_URL, json={"text": doc["text"]})
        if resp.status_code != 200:
            print("Error API")
            continue
        vector = resp.json()["vector"]
        
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=doc["id"],
                    vector=vector,
                    payload={"contenido": doc["text"]}
                )
            ]
        )
        print("✅ Guardado.")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n💾 ¡Carga completada!")
