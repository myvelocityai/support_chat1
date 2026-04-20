from langchain_core.prompts import ChatPromptTemplate
from myvelocity_ai_chatbot.services.claude_llm_service import get_llm

PROMPT = ChatPromptTemplate.from_template("""
You are a helpful tax software support assistant.
Use the following context to answer the question.
If the context does not contain relevant information to answer the question,
respond with: "I'm sorry, I can't help with that. Please contact our support team for further assistance."

Rules for your response:
- Do not use markdown formatting (no ##, **, ---, >, or emoji)
- Do not use headers
- Write steps as plain numbered list: 1. 2. 3.
- Write causes as plain numbered list: 1. 2. 3.
- Keep the tone simple and professional
- Do not add tips or extra sections not found in the context

Context:
{context}

Question:
{question}

Answer:
""")

llm = get_llm()

async def ask_question(query: str, retriever):
    docs = retriever.invoke(query)

    if not docs:
        return {
            "answer": "I'm sorry, I can't help with that. Please contact our support team for further assistance.",
            "sources": []
        }

    context = "\n\n".join([doc.page_content for doc in docs])

    final_prompt = PROMPT.format(
        context=context,
        question=query
    )

    response = await llm.ainvoke(final_prompt)

    return {
        "answer": response.content,
        "sources": [doc.page_content[:200] for doc in docs]
    }