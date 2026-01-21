from pydantic import BaseModel
class EmbeddingRequest(BaseModel):
    text: str
class EmbeddingResponse(BaseModel):
    vector: list[float]
    dimension: int