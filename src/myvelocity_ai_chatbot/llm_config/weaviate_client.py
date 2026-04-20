import weaviate
import weaviate.classes as wvc

from myvelocity_ai_chatbot.configs.logger import setup_logger, get_logger
from myvelocity_ai_chatbot.configs.settings import WEAVIATE_URL, WEAVIATE_API_KEY
from weaviate.classes.init import Auth

#log setup
setup_logger()
logger = get_logger(__name__)

def get_client():
    try:
        print(f"Connecting to {WEAVIATE_URL}")
        logger.info(f"Connecting to {WEAVIATE_URL}", service="get_client")
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=WEAVIATE_URL,
            auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
            additional_config=wvc.init.AdditionalConfig(
                timeout=wvc.init.Timeout(init=30)
            ),
            skip_init_checks=True
        )
        logger.info(f"Connected to {client.is_ready()}", service="get_client")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to {WEAVIATE_URL}, {e}", service="get_client")
        raise

