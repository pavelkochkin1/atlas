from exploitation_agent.model import exploitation_agent
from exploration_agent.draft_creation import process_tables
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/create_drafts")
def create_drafts_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_tables)
    return {"status": "started create drafts"}


@app.get("/")
def answer_question(question: str):
    response = exploitation_agent.invoke({"query": question})
    return {"result": response["result"]}
