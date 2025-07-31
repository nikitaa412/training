from fastapi import FastAPI, UploadFile, File
from rag_qna import answer_question
from rag_summarizer import summarize_document
import tempfile

app = FastAPI()

@app.post("/ask")
async def ask_question(file: UploadFile = File(...), question: str = ""):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    return answer_question(tmp_path, question)

@app.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    return summarize_document(tmp_path)
