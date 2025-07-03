# backend/routes/chat_cree.py

from fastapi import APIRouter
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

# 🔓 Load CREE vector DB
vectorstore = FAISS.load_local(
    "backend/cree_vectore",
    HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
    index_name="index",
    allow_dangerous_deserialization=True
)

# 📄 Prompt template (customized for CREE)
QA_TEMPLATE = """
You are an internal assistant for the CREE regulatory reporting project.
Use the following Confluence documentation and Jira notes to answer developer questions.

Context:
{context}

Question:
{question}
"""

prompt = PromptTemplate(input_variables=["context", "question"], template=QA_TEMPLATE)

# 🧠 Local model
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_new_tokens=256)
llm = HuggingFacePipeline(pipeline=pipe)

# 🔁 CREE chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": prompt}
)

class ChatRequest(BaseModel):
    question: str

@router.post("/chat/cree")
async def chat_cree(request: ChatRequest):
    response = qa_chain.run(request.question)
    return {"answer": response}
