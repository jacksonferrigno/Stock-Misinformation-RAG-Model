from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm_driver import generate_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class QueryRequest(BaseModel):
    query: str
    ticker: str

@app.post("/generate")
async def generate(query_req: QueryRequest):
    try:
        result = generate_response(query_req.query, query_req.ticker.upper())
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/")
async def root():
    return {"status": "all systems running"}
