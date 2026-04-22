from pydantic import BaseModel, Field
from typing import List

class QueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    cached: bool = False