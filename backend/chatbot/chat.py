from fastapi import APIRouter
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from dotenv import load_dotenv

# Load environment variables (if needed)
load_dotenv()

router = APIRouter()

# 🔓 Load FAISS vector DB (you already created this with HuggingFace embeddings)
vectorstore = FAISS.load_local(
    "backend/vectore",
    HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
    index_name="index",
    allow_dangerous_deserialization=True
)

# 📄 Prompt template
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

# ✅ Local model: google/flan-t5-base
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Create pipeline
pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=256
)

# Wrap the pipeline into LangChain LLM
llm = HuggingFacePipeline(pipeline=pipe)

# 🔁 Retrieval QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": prompt}
)

# 💬 Request schema
class ChatRequest(BaseModel):
    question: str

# 🚀 /api/chat endpoint
@router.post("/chat")
async def chat(request: ChatRequest):
    response = qa_chain.run(request.question)
    return {"answer": response}
