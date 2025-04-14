import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm_driver import generate_response
from fastapi.middleware.cors import CORSMiddleware



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://stock-misinform-frontend.vercel.app",
        "http://localhost:3000"  # Keep for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        print(f"[ERROR] LLM generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/")
async def root():
    return {"status": "all systems running"}
