# rag_agent.py
import requests
from llm_simulator import MockLLM # Importamos nuestro cerebro falso

# --- CONFIGURACIÓN DE INFRAESTRUCTURA ---
EMBEDDING_API_URL = "http://127.0.0.1:8080/embed"
QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_NAME = "conocimiento_base"

# Instanciamos el "Cerebro Generativo"
llm = MockLLM()

def run_rag_pipeline(user_query):
    print(f"\n👤 USUARIO: {user_query}")
    print("-" * 50)

    # ---------------------------------------------------------
    # FASE 1: RETRIEVAL (Recuperación - El Buscador)
    # ---------------------------------------------------------
    print("1️⃣  [Agent] Vectorizando pregunta...")
    try:
        # Paso A: Texto -> Vector
        emb_resp = requests.post(EMBEDDING_API_URL, json={"text": user_query})
        query_vector = emb_resp.json()["vector"]

        # Paso B: Vector -> Documentos (Qdrant vía HTTP)
        print("2️⃣  [Agent] Buscando en memoria (Qdrant)...")
        search_url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points/search"
        payload = {
            "vector": query_vector,
            "limit": 1, # Solo queremos el mejor resultado para el contexto
            "with_payload": True
        }
        
        search_resp = requests.post(search_url, json=payload)
        resultados = search_resp.json().get("result", [])

    except Exception as e:
        print(f"❌ Error en la fase de Retrieval: {e}")
        return

    # ---------------------------------------------------------
    # FASE 2: AUGMENTATION (Preparar el contexto)
    # ---------------------------------------------------------
    context_text = ""
    if resultados:
        best_match = resultados[0]
        context_text = best_match["payload"]["contenido"]
        score = best_match["score"]
        print(f"✅ [RAG] Contexto encontrado (Confianza: {score:.2f}):")
        print(f"    📄 '{context_text}'")
    else:
        print("⚠️ [RAG] No se encontró contexto relevante.")

    # ---------------------------------------------------------
    # FASE 3: GENERATION (Generación - El LLM)
    # ---------------------------------------------------------
    print("3️⃣  [Agent] Enviando datos al LLM para redacción...")
    
    # Aquí es donde ocurre la magia. Le damos al LLM la pregunta Y la respuesta encontrada.
    respuesta_final = llm.generate_response(
        user_query=user_query, 
        retrieved_context=context_text
    )

    print("-" * 50)
    print(f"🤖 IA: {respuesta_final}")
    print("-" * 50)

# --- BUCLE DE CONVERSACIÓN ---
if __name__ == "__main__":
    # Escenario 1: Pregunta sobre Pizza
    run_rag_pipeline("¿Qué opinas de la comida italiana?")
    
    # Escenario 2: Pregunta sobre Tecnología
    run_rag_pipeline("Dime algo sobre lenguajes de backend")