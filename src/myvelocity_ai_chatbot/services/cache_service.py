import weaviate.classes as wvc
from myvelocity_ai_chatbot.configs.logger import get_logger

logger = get_logger(__name__)

CACHE_COLLECTION = "AnswerCache"
SIMILARITY_THRESHOLD = 0.92


def ensure_cache_collection(client):
    if not client.collections.exists(CACHE_COLLECTION):
        client.collections.create(
            name=CACHE_COLLECTION,
            properties=[
                wvc.config.Property(name="query", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="answer", data_type=wvc.config.DataType.TEXT),
            ],
            vectorizer_config=wvc.config.Configure.Vectorizer.none(),
        )
        logger.info(f"Created {CACHE_COLLECTION} collection", service="cache_service")


def get_cached_answer(query: str, client, embeddings) -> str | None:
    try:
        vector = embeddings.embed_query(query)
        collection = client.collections.get(CACHE_COLLECTION)
        result = collection.query.near_vector(
            near_vector=vector,
            limit=1,
            certainty=SIMILARITY_THRESHOLD,
            return_properties=["query", "answer"],
        )
        if result.objects:
            cached = result.objects[0].properties
            logger.info(f"Cache hit for query: {query[:60]}", service="cache_service")
            return cached["answer"]
    except Exception as e:
        logger.error(f"Cache lookup failed: {e}", service="cache_service")
    return None


def store_answer(query: str, answer: str, client, embeddings):
    try:
        vector = embeddings.embed_query(query)
        collection = client.collections.get(CACHE_COLLECTION)
        collection.data.insert(
            properties={"query": query, "answer": answer},
            vector=vector,
        )
        logger.info(f"Cached answer for query: {query[:60]}", service="cache_service")
    except Exception as e:
        logger.error(f"Cache store failed: {e}", service="cache_service")
