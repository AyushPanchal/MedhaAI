from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Initialize the model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Define the intent classification prompt
intent_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an intent classifier for MedhaAI — a chatbot assistant for the Computer Science Department at SVNIT Surat.\n"
     "Your task is to classify the user's query into one of the following intents:\n"
     "- academic_query\n"
     "- course_syllabus\n"
     "- faculty_details\n"
     "- lab_info\n"
     "- timetable\n"
     "- placement_statistics\n"
     "- contact_info\n"
     "\n"
     "Respond ONLY with the intent name. Do not explain."),
    ("human", "{input}")
])

# Create the runnable chain
intent_classifier = intent_prompt | llm | StrOutputParser()


# Optionally: wrapper function
def classify_intent(user_query: str) -> str:
    return intent_classifier.invoke({"input": user_query})
