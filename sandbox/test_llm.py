from src.llms.openai_llm import get_openai_chat_model


def test_llm_basic():
    llm = get_openai_chat_model()
    query = "Explain what OpenAI is in one sentence."
    response = llm.invoke(query)
    print("Response:\n", response.content)


if __name__ == "__main__":
    test_llm_basic()
