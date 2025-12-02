import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableParallel,
    RunnableLambda,
)
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
parser = StrOutputParser()

# Store actual chat messages
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# Proper chat-style prompt with history as messages
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Use the conversation history to respond to the new user message.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

# Return just the history list, not an extra dict
def get_memory(_):
    return memory.load_memory_variables({})["history"]

# Wire history + current question into the prompt
chain = (
    RunnableParallel(
        history=RunnableLambda(get_memory),
        question=RunnablePassthrough(),
    )
    | prompt
    | llm
    | parser
)

st.set_page_config(page_title="Chatbot", page_icon="💬")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💬 Chatbot with Memory (Runnable Version)")

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

user_input = st.chat_input("Type something...")

if user_input:
    # UI history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Run chain with memory
    result = chain.invoke(user_input)

    # Save to LangChain memory (for next turns)
    memory.save_context({"question": user_input}, {"output": result})

    # UI assistant message
    st.session_state.messages.append({"role": "assistant", "content": result})

    st.rerun()
