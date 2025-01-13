from fastapi import FastAPI, HTTPException, Depends , Request
from dotenv import load_dotenv
from utils import load_vectorstore
import os

load_dotenv()
vectorstore = load_vectorstore(vectorstore_path="shopify_langchain_testing_vectorstore",index_name="products")
app = FastAPI()

def verify_api_key(request : Request):
    token = request.headers.get("Authorization")

    if not token :
        raise HTTPException(status_code=401,detail="No api key provided in the header")
    
    token_str= token.split(" ")[1]
    print(token_str)
    if token_str == os.getenv("SHOPIFY_API_KEY"):
        return token
    else:
        raise HTTPException(status_code=401,detail="Invalid api key")

@app.get("/product_search")
async def product_search(query: str, token: str = Depends(verify_api_key)):
    try:
        result = vectorstore.similarity_search(query, k=5)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))