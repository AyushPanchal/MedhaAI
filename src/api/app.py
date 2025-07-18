from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.pipelines.main_rag_pipeline import run_medha_query

app = FastAPI()

# Allow CORS (for Streamlit frontend to access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response schema
class QueryRequest(BaseModel):
    query: str
    chat_history: list  # List of dicts with `type` and `content`


@app.post("/query")
def query_medha(data: QueryRequest):
    # Convert list of dicts to LangChain message objects
    from langchain_core.messages import HumanMessage, AIMessage
    history_msgs = []
    for msg in data.chat_history:
        if msg["type"] == "human":
            history_msgs.append(HumanMessage(content=msg["content"]))
        elif msg["type"] == "ai":
            history_msgs.append(AIMessage(content=msg["content"]))

    result = run_medha_query(data.query, history_msgs)
    return {
        "intent": result["intent"],
        "answer": result["answer"],
        "chat_history": [{"type": m.type, "content": m.content} for m in result["chat_history"]]
    }
