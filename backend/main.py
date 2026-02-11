from fastapi import FastAPI
from agents.planner_agent import PlannerAgent
from agents.search_agent import SearchAgent
from services.pdf_reader import PDFReader
import os
from services.vector_service import VectorService
from agents.summarizer_agent import SummarizerAgent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ResearchPilot AI Agent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


planner = PlannerAgent()
search_agent = SearchAgent()
pdf_reader = PDFReader()
vector_service = VectorService()
summarizer = SummarizerAgent()

@app.on_event("startup")
def startup():
    print("🚀 ResearchPilot backend started")

@app.get("/")
def root():
    return {"message": "ResearchPilot backend is running"}

@app.post("/research/plan")
def create_research_plan(goal: str):
    return planner.create_plan(goal)

@app.post("/research/search")
def search_research_papers(goal: str):
    papers = search_agent.search_papers(goal)
    return {
        "query": goal,
        "papers": papers
    }

@app.post("/research/read")
def read_paper(pdf_url: str):
    try:
        text = pdf_reader.extract_text(pdf_url)

        if not text:
            return {"error": "Unable to extract text from this PDF."}

        vector_service.store(text)

        return {
            "pdf_url": pdf_url,
            "message": "PDF processed successfully",
            "text_length": len(text)
        }

    except Exception as e:
        return {"error": str(e)}

@app.post("/research/ask")
def ask_question(question: str, depth: int = 5):
    chunks = vector_service.semantic_search(question, k=depth + 2)

    if not chunks:
        return {
            "error": "No research paper loaded. Please upload a PDF first."
        }

    summary = summarizer.summarize(chunks, max_points=depth)

    return {
        "question": question,
        "summary": summary
    }


