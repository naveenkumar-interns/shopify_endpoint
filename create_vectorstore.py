from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import FAISS
import os
# Define the metadata extraction function.

load_dotenv()

def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["id"] = record.get("id")
    metadata["title"] = record.get("title")
    metadata["tags"] = record.get("tags")
    metadata["image_list"] = record.get("image_list")
    metadata["handle"] = record.get("handle")
    return metadata

def create_vectorstore(documents,embeddings):
    vectorstore = FAISS.from_documents(documents=documents,embedding=embeddings)
    return vectorstore
 
def save_vectorstore(vectorstore,save_path,index_name):
    vectorstore.save_local(save_path,index_name)
    print("vectorstore saved to : ", save_path)
    return None



if __name__== "__main__":

    loader = JSONLoader(
    file_path='./products.json',
    jq_schema='.[]',
    content_key="expanded_description",
    metadata_func=metadata_func
)
        
    documents = loader.load()
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = create_vectorstore(documents,embeddings)
    save_vectorstore(vectorstore,save_path = "shopify_langchain_testing_vectorstore",index_name = "products")



