from langchain_community.embeddings import FastEmbedEmbeddings


def get_embeddings():
    return FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
