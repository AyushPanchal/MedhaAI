from src.pipelines.main_rag_pipeline import run_medha_query

chat_history = []

while True:
    query = input("\n🔍 Ask MedhaAI: ").strip()
    if query.lower() in {"exit", "quit"}:
        break
    result = run_medha_query(query, chat_history)
    print(f"\n🧠 Intent: {result['intent']}")
    print(f"📤 Answer: {result['answer']}")

# hello, who are you?
# Who is the hod ?
# list down all of her research interests
# who was the hod before her ?