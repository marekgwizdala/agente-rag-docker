from fastapi import FastAPI
from app.schemas import EmbeddingRequest, EmbeddingResponse
from app.services import EmbeddingModel

app = FastAPI(title="AI Embedding Service")
model_service = EmbeddingModel()

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Fuerza en GCP, potente es."}

@app.post("/embed", response_model=EmbeddingResponse)
def create_embedding(request: EmbeddingRequest):
    vector = model_service.get_embedding(request.text)
    return EmbeddingResponse(vector=vector, dimension=len(vector))