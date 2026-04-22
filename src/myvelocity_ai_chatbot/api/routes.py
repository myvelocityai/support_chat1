from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from myvelocity_ai_chatbot.models.schema import QueryRequest, QueryResponse
from myvelocity_ai_chatbot.services.rag_service import ask_question

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


@router.post("/chat", response_model=QueryResponse)
@limiter.limit("10/minute")
async def chat(req: QueryRequest, request: Request):
    result = await ask_question(
        req.query,
        request.app.state.retriever,
        request.app.state.weaviate_client,
        request.app.state.embeddings,
    )
    return result


@router.delete("/cache")
async def clear_cache(request: Request):
    client = request.app.state.weaviate_client
    client.collections.delete("AnswerCache")
    from myvelocity_ai_chatbot.services.cache_service import ensure_cache_collection
    ensure_cache_collection(client)
    return {"message": "Cache cleared"}
