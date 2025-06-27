from fastapi import APIRouter
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Load vectorstore (still using HuggingFace embeddings for retrieval only)
vectorstore = FAISS.load_local(
    "backend/vectore",
    HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
    index_name="index",
    allow_dangerous_deserialization=True
)

# Prompt template
QA_TEMPLATE = """
You are an internal project assistant helping developers onboard and understand a codebase.
Use the following project documentation and Jira notes to answer the question.
If you don't know, say "I don't know."

Context:
{context}

Question:
{question}
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=QA_TEMPLATE
)

# Used OpenAI's LLM
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")  # or "gpt-4" if your subscription allows

# QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": prompt}
)

# Request schema
class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
async def chat(request: ChatRequest):
    response = qa_chain.run(request.question)
    return {"answer": response}
