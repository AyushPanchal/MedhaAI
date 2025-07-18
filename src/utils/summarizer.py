# src/utils/summarizer.py
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

summary_prompt = PromptTemplate.from_template("""
You are a helpful assistant. Summarize the following conversation so far into a concise memory for future reference.

Chat History:
{chat_history}

Summary:
""")

summarize_chain = LLMChain(llm=llm, prompt=summary_prompt)


def summarize_chat_history(chat_history_messages) -> str:
    # Convert messages to plain text
    formatted = ""
    for m in chat_history_messages:
        role = "User" if m.type == "human" else "Assistant"
        formatted += f"{role}: {m.content}\n"

    result = summarize_chain.run(chat_history=formatted.strip())
    return result
