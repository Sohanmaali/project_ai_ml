import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
parser = StrOutputParser()

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.title("💬 Chatbot")

msgs = StreamlitChatMessageHistory(key="chat_history")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Use the conversation history to respond. Keep responses concise.",
        ),
        ("human", "{input}"),
    ]
)

base_chain = prompt | llm | parser
st.chat_message("user").markdown("hy, how can help you!")


for msg in msgs.messages:
    role = "user" if msg.type == "human" else "assistant"
    st.chat_message(role).markdown(msg.content)

user_input = st.chat_input("Type something...")

if user_input:
    st.chat_message("user").markdown(user_input)

    msgs.add_user_message(user_input)

    history_text = ""
    for m in msgs.messages[:-1]:
        if m.type == "human":
            history_text += f"User: {m.content}\n"
        else:
            history_text += f"Assistant: {m.content}\n"

    final_prompt = f"{history_text}User: {user_input}"
    ai_response = base_chain.invoke({"input": final_prompt})

    msgs.add_ai_message(ai_response)

    st.rerun()
