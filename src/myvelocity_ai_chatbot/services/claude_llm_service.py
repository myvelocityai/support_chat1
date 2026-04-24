import anthropic
from myvelocity_ai_chatbot.configs.settings import ANTHROPIC_API_KEY

_client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_INSTRUCTIONS = """You are a helpful tax software support assistant for TicTacTax.
Your job is to help users with tax software questions, tax filing issues, and general tax guidance.

When answering:
1. If the provided context is relevant, use it as your primary source.
2. If the context is not relevant or incomplete, answer using your general tax knowledge.
3. Only say you cannot help if the question is completely unrelated to taxes or tax software.

Rules for your response:
- Do not use markdown formatting (no ##, **, ---, >, or emoji)
- Do not use headers
- Write steps as plain numbered list: 1. 2. 3.
- Keep the tone simple and professional
- Be concise and direct"""


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
