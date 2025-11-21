from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import rag
from fastapi.middleware.cors import CORSMiddleware
from groq import InternalServerError

client = Groq(api_key="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")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_question(q: Query):
    context = rag.search(q.question)
    
    prompt = f"""
    You are a chatbot answering questions about the developer.
    Use only the following information:
    {context}
    Question: {q.question}
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content

    except InternalServerError as e:
        # Groq-side failure
        print(e)
        return  {"answer": "Groq API is currently experiencing a server-side error (500). Please try again shortly."} 

    except Exception as e:
        # Anything else
        print(e)
        return {"answer": "Unexpected error"} 

@app.get("/")
def ask_question():
    print("i am herer with quesy")   
    return {"answer": "I am working"}
