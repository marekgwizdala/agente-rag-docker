# llm_simulator.py
import time

class MockLLM:
    def __init__(self):
        print("🤖 [LLM] Inicializando núcleo de generación simulada...")

    def generate_response(self, user_query, retrieved_context):
        """
        Simula lo que haría GPT-4: Leer el contexto y responder la pregunta.
        """
        print("   Thinking... (Simulando latencia de GPU)")
        time.sleep(1) # Un poco de drama para sentir el realismo
        
        # PROMPT ENGINEERING (Así se vería el prompt real)
        # ------------------------------------------------
        # System: Eres un asistente útil. Usa el contexto para responder.
        # Context: {retrieved_context}
        # User: {user_query}
        # ------------------------------------------------
        
        # GENERACIÓN (Simulada con lógica de plantillas)
        if not retrieved_context:
            return "Lo siento, mis bancos de memoria no encontraron información sobre eso."
        
        # Aquí fingimos que la IA "leyó" y "entendió"
        respuesta = (
            f"¡Hola! He analizado tu base de conocimientos.\n"
            f"Basado en el documento que dice: '{retrieved_context}'...\n"
            f"Puedo responder a tu pregunta '{user_query}' confirmando que esa es la información relevante."
        )
        
        return respuesta