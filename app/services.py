import random
import time
import zlib

class EmbeddingModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingModel, cls).__new__(cls)
            print("⚡ [Keyword-Aware Mode] Cargando modelo inteligente simulado...")
        return cls._instance

    def get_embedding(self, text: str):
        time.sleep(0.05)
        text_lower = text.lower()
        
        # TRUCO DE ARQUITECTO:
        # Forzamos semillas específicas según el tema.
        # Esto imita la "búsqueda semántica" sin gastar RAM.
        if "docker" in text_lower:
            seed_value = 1001 # Vector exclusivo para Docker
        elif "pizza" in text_lower or "comida" in text_lower:
            seed_value = 2002 # Vector exclusivo para Pizza
        elif "python" in text_lower or "backend" in text_lower:
            seed_value = 3003 # Vector exclusivo para Python/Backend
        elif "nube" in text_lower or "cloud" in text_lower or "aws" in text_lower or "oracle" in text_lower:
            seed_value = 4004 # Vector para Cloud
        else:
            # Si no es nada conocido, usamos el hash genérico
            seed_value = zlib.adler32(text.encode('utf-8'))

        random.seed(seed_value)
        return [random.random() for _ in range(384)]
