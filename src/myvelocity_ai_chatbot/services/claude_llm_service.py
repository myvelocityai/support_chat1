from langchain_anthropic import ChatAnthropic
from myvelocity_ai_chatbot.configs.settings import ANTHROPIC_API_KEY

def get_llm():
    print(ANTHROPIC_API_KEY[:10])
    return ChatAnthropic(api_key=ANTHROPIC_API_KEY, model_name="claude-sonnet-4-6", temperature=0.2)

