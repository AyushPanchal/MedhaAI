from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableMap
from langchain_core.output_parsers import StrOutputParser

from src.retrievers.intent_retriever import get_retriever_for_intent

from dotenv import load_dotenv

load_dotenv()


def build_intent_routed_rag_chain():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)

    # Updated QA Prompt with memory support
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Your name is Medha and you are a helpful assistant for SVNIT Surat.\n"
         "Use the provided memory, context, and chat history to answer the user's question.\n"
         "If the answer is not found, reply with 'I don't know'. Do not hallucinate.\n\n"
         "Memory:\n{memory}"),
        MessagesPlaceholder("chat_history"),
        ("human", "Context:\n{context}\n\nQuestion: {question}")
    ])

    # Document retriever based on intent
    def retrieve_docs_by_intent(inputs):
        intent = inputs["intent"]
        query = inputs["input"]
        retriever = get_retriever_for_intent(intent)
        return retriever.invoke(query)

    # Final QA chain with memory, context, and history
    qa_chain = qa_prompt | llm | StrOutputParser()

    full_chain = RunnableMap({
        "question": lambda x: x["input"],
        "context": retrieve_docs_by_intent,
        "chat_history": lambda x: x["chat_history"],
        "memory": lambda x: x.get("memory", "")  # fallback to empty string if no memory
    }) | qa_chain

    return full_chain
