from myvelocity_ai_chatbot.services.claude_llm_service import call_claude
from myvelocity_ai_chatbot.services.cache_service import get_cached_answer, store_answer

FALLBACK = "I'm sorry, I can't help with that. Please contact our support team for further assistance."


async def ask_question(query: str, retriever, client, embeddings):
    cached = get_cached_answer(query, client, embeddings)
    if cached:
        return {"answer": cached, "sources": [], "cached": True}

    docs = retriever.invoke(query)

    if not docs:
        return {"answer": FALLBACK, "sources": [], "cached": False}

    context = "\n\n".join([doc.page_content for doc in docs])

    answer = await call_claude(context, query)

    store_answer(query, answer, client, embeddings)

    return {
        "answer": answer,
        "sources": [doc.page_content[:200] for doc in docs],
        "cached": False,
    }
