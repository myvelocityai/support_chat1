from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from myvelocity_ai_chatbot.api.routes import router, limiter
from myvelocity_ai_chatbot.llm_config.weaviate_client import get_client
from myvelocity_ai_chatbot.llm_config.embeddings import get_embeddings
from myvelocity_ai_chatbot.services.retriever import build_retriever
from myvelocity_ai_chatbot.services.cache_service import ensure_cache_collection

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    client = get_client()
    embeddings = get_embeddings()
    ensure_cache_collection(client)
    app.state.weaviate_client = client
    app.state.embeddings = embeddings
    app.state.retriever = build_retriever(client, embeddings)

@app.on_event("shutdown")
async def shutdown():
    client = app.state.weaviate_client
    if client:
        client.close()

app.include_router(router)
