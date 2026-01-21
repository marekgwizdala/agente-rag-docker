import os
from groq import Groq

class RealLLM:
    def __init__(self, api_key):
        # Inicializamos el cliente con la llave que nos pase el usuario
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile" # Usamos Llama 3 (Rápido y listo)

    def generate_response(self, user_query, retrieved_context):
        # 1. Construimos el Prompt de Arquitecto
        # Le damos instrucciones precisas de comportamiento (System Prompt)
        system_prompt = (
            "Eres un Asistente de Soluciones IA experto y amable. "
            "Tu tarea es responder a la pregunta del usuario BASÁNDOTE ÚNICAMENTE en el contexto proporcionado. "
            "Si el contexto no tiene la respuesta, di 'No tengo información sobre eso en mis documentos'. "
            "No inventes cosas."
        )

        user_message = f"""
        Contexto Recuperado:
        {retrieved_context}

        Pregunta del Usuario:
        {user_query}
        """

        try:
            # 2. Llamada a la API Real
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                model=self.model,
                temperature=0.5, # Creatividad balanceada
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error conectando con Groq: {e}"