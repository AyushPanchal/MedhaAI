from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableMap
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

INDEX_DIR = r"C:\Users\Ayush\OneDrive\Desktop\MedhaAI\faiss_index"
RETRIEVAL_TOP_K = 25

def build_custom_conversational_rag_chain():
    # Load LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)

    # Load vector store and embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vectorstore = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": RETRIEVAL_TOP_K})

    # Prompt for answering with context + history
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Your name is Medha and you are a helpful chatbot assistant with expertise in answering questions about SVNIT, Surat.\n"
         "Use ONLY the provided context and chat history to answer the user's query.\n"
         "Only provide the latest information. \n"
         "If the answer is not in the context, reply with 'I don't know.' Do not hallucinate."),
        MessagesPlaceholder("chat_history"),
        ("human", "Context:\n{context}\n\nQuestion: {question}")
    ])

    # Chain to retrieve documents
    def retrieve_documents(inputs):
        docs = retriever.invoke(inputs["input"])
        context = "\n\n".join([doc.page_content for doc in docs])
        return {"context": context, "documents": docs}

    # QA chain: generate answer using context
    qa_chain = qa_prompt | llm | StrOutputParser()

    # Full chain with doc tracking
    full_chain = RunnableMap({
        "question": lambda x: x["input"],
        "chat_history": lambda x: x["chat_history"],
        "retrieved": retrieve_documents
    }) | RunnableMap({
        "question": lambda x: x["question"],
        "context": lambda x: x["retrieved"]["context"],
        "chat_history": lambda x: x["chat_history"],
        "documents": lambda x: x["retrieved"]["documents"]
    }) | RunnableMap({
        "answer": qa_chain,
        "sources": lambda x: [
            doc.metadata.get("source", "Unknown Source") for doc in x["documents"]
        ]
    })

    return full_chain
