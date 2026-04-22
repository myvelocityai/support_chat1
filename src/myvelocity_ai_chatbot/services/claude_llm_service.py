import anthropic
from myvelocity_ai_chatbot.configs.settings import ANTHROPIC_API_KEY

_client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_INSTRUCTIONS = """You are a helpful tax software support assistant.
Use the context provided in the user message to answer the question.
If the context does not contain relevant information to answer the question,
respond with: "I'm sorry, I can't help with that. Please contact our support team for further assistance."

Rules for your response:
- Do not use markdown formatting (no ##, **, ---, >, or emoji)
- Do not use headers
- Write steps as plain numbered list: 1. 2. 3.
- Write causes as plain numbered list: 1. 2. 3.
- Keep the tone simple and professional
- Do not add tips or extra sections not found in the context"""


async def call_claude(context: str, question: str) -> str:
    response = await _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": SYSTEM_INSTRUCTIONS,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}",
            }
        ],
    )
    return response.content[0].text
