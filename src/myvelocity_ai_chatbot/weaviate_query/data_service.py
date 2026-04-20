from myvelocity_ai_chatbot.services.retriever import get_retriever
from myvelocity_ai_chatbot.services.claude_llm_service import get_llm

retriever = get_retriever()
llm = get_llm()

PROMPT = """
You are a precise assistant.

Use ONLY the context below.
If answer is not found, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""

def ask(query: str):
    docs = retriever.get_relevant_documents(query)

    if not docs:
        return "I don't know"

    context = "\n\n".join([
        doc.page_content for doc in docs
    ])

    final_prompt = PROMPT.format(
        context=context,
        question=query
    )

    response = llm.invoke(final_prompt)

    return response.content