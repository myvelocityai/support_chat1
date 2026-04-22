from  myvelocity_ai_chatbot.configs.settings import WEAVIATE_INDEX
from langchain_weaviate import WeaviateVectorStore

def build_retriever(client, embeddings):
    vectorstore = WeaviateVectorStore(
        client=client,
        index_name=WEAVIATE_INDEX,
        text_key="content",
        embedding=embeddings,
    )

    result = client.collections.get(WEAVIATE_INDEX).query.fetch_objects(limit=200)
    print(f"Total objects: {len(result.objects)}")

    sources = set()
    for obj in result.objects:
        sources.add(obj.properties.get("source", "unknown"))

    print("Ingested files:")
    for s in sources:
        print(f"result of data source", s)

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )