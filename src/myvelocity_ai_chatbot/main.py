from dotenv import load_dotenv
#load env
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from myvelocity_ai_chatbot.api.routes import router
from myvelocity_ai_chatbot.llm_config.weaviate_client import get_client
from myvelocity_ai_chatbot.services.retriever import build_retriever

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    client = get_client()
    app.state.weaviate_client = client
    app.state.retriever = build_retriever(client)

@app.on_event("shutdown")
async def shutdown():
    client = app.state.weaviate_client
    if client:
        client.close()

app.include_router(router)