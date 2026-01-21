import streamlit as st
import requests
# from llm_simulator import MockLLM  <-- ADIÓS SIMULADOR
from llm_real import RealLLM       # <-- HOLA REALIDAD

# --- CONFIGURACIÓN ---
ST_API_URL = "http://127.0.0.1:8080/embed"
ST_QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_NAME = "conocimiento_base"

st.set_page_config(page_title="AI Architect Chat", page_icon="🧠")

st.title("🧠 Asistente RAG con Llama 3")
st.caption("Arquitectura: Streamlit -> FastAPI -> Qdrant -> GROQ (Llama3)")

# --- SIDEBAR: CONFIGURACIÓN ---
with st.sidebar:
    st.header("🔐 Configuración")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    st.markdown("[Obtener Key Gratis](https://console.groq.com/keys)")
    
    if not api_key:
        st.warning("👈 Por favor ingresa tu API Key para activar el cerebro.")

# --- INICIALIZACIÓN DEL CEREBRO ---
if "llm" not in st.session_state or st.session_state.get("api_key") != api_key:
    if api_key:
        st.session_state.llm = RealLLM(api_key)
        st.session_state.api_key = api_key
        st.success("Cerebro Llama-3 Activado 🚀")
    else:
        st.session_state.llm = None

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LÓGICA RAG ---
def get_rag_response(user_query):
    if not st.session_state.llm:
        return "⚠️ Necesito la API Key para pensar."

    # 1. Retrieval
    try:
        resp = requests.post(ST_API_URL, json={"text": user_query})
        query_vector = resp.json()["vector"]
    except:
        return "Error en API Embeddings."

    # 2. Search
    try:
        search_url = f"{ST_QDRANT_URL}/collections/{COLLECTION_NAME}/points/search"
        payload = {"vector": query_vector, "limit": 1, "with_payload": True}
        search_resp = requests.post(search_url, json=payload)
        resultados = search_resp.json().get("result", [])
    except:
        return "Error en Qdrant."

    # 3. Generation
    context_text = ""
    if resultados:
        best_match = resultados[0]
        context_text = best_match["payload"]["contenido"]
        # Mostrar Debug
        with st.expander("🕵️ Lo que encontró el buscador (Contexto)"):
            st.info(f"{context_text}")
    else:
        with st.expander("🕵️ Contexto"):
            st.warning("No encontré documentos relevantes.")

    # Llamada al LLM Real
    return st.session_state.llm.generate_response(user_query, context_text)

# --- CHAT ---
if prompt := st.chat_input("Pregunta algo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consultando a Llama 3..."):
            response = get_rag_response(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})