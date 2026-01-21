import requests
# Nota: Ya no importamos QdrantClient porque nos ha traicionado.

# Configuración
EMBEDDING_API_URL = "http://localhost:8080/embed"
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "conocimiento_base"

def buscar_conocimiento(pregunta, top_k=2):
    print(f"\n🔎 Preguntando: '{pregunta}'")
    
    try:
        # 1. VECTORIZAR (Esto sigue igual, llamamos a tu API)
        resp = requests.post(EMBEDDING_API_URL, json={"text": pregunta})
        if resp.status_code != 200:
            print(f"❌ Error API Embeddings: {resp.text}")
            return
        
        query_vector = resp.json()["vector"]

        # 2. BÚSQUEDA (EL CAMBIO MAESTRO)
        # En lugar de usar la librería python, golpeamos la API REST de Qdrant directamente.
        # Documentación: POST /collections/{name}/points/search
        qdrant_search_url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points/search"
        
        payload = {
            "vector": query_vector,
            "limit": top_k,
            "with_payload": True # Para que nos devuelva el texto original
        }
        
        search_resp = requests.post(qdrant_search_url, json=payload)
        
        if search_resp.status_code != 200:
            print(f"❌ Error Qdrant API: {search_resp.text}")
            return

        resultados = search_resp.json().get("result", [])

        # 3. MOSTRAR RESULTADOS
        print(f"   Resultados encontrados:")
        for hit in resultados:
            score = hit["score"]
            # En la API REST, el payload viene dentro de un diccionario 'payload'
            texto = hit["payload"]["contenido"]
            print(f"   🌟 [Similitud: {score:.4f}] -> {texto}")
            
    except Exception as e:
        print(f"💀 Error crítico: {e}")

# --- EJECUCIÓN ---
if __name__ == "__main__":
    buscar_conocimiento("Quiero comer algo italiano")
    buscar_conocimiento("herramientas para la nube")
    buscar_conocimiento("programación backend")