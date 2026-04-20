from fastapi import APIRouter, Request
from myvelocity_ai_chatbot.models.schema import QueryRequest, QueryResponse
from myvelocity_ai_chatbot.services.rag_service import ask_question

router = APIRouter()

@router.post("/chat", response_model=QueryResponse)
async def chat(req: QueryRequest, request: Request):
    retriever = request.app.state.retriever

    result = await ask_question(req.query, retriever)

    return result