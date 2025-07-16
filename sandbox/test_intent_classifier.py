from src.router.intent_classifier import classify_intent


query = "What is the syllabus of CO402?"
intent = classify_intent(query)
print("Predicted intent:", intent)
