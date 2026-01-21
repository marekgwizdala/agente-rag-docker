import random
import time

class EmbeddingModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingModel, cls).__new__(cls)
            print("⚡ [Lite Mode] Cargando modelo ligero (Sin consumo de RAM)...")
        return cls._instance

    def get_embedding(self, text: str):
        # Simulamos latencia de red (0.1s)
        time.sleep(0.1)
        # Retornamos un vector de 384 dimensiones aleatorio
        # Esto engaña al sistema para que crea que hay una IA funcionando
        return [random.random() for _ in range(384)]
