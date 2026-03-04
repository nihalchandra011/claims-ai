from backend.web_search import ollama_web_search
from backend.llm_local import local_llm_generate
from backend.router import classify_question
import concurrent.futures


def build_prompt(context, question):

    prompt = f"""
You are ClaimsAI, an expert healthcare claims and contract analyst.

Explain clearly and use bullet points when helpful.

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt


def agent_answer(metadata: dict, user_question: str):

    route = classify_question(user_question)

    context = ""

    # CLAIM QUESTIONS
    if route == "claims":
        context = "Healthcare claims domain knowledge."

    # ERROR QUESTIONS
    elif route == "errors":
        context = "Healthcare claim rejection and denial analysis."

    # CONTRACT QUESTIONS
    elif route == "contract":
        context = "Healthcare payer-provider contracts."

    # GENERAL QUESTIONS → WEB SEARCH
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:

            search_future = executor.submit(
                ollama_web_search,
                user_question
            )

            context = search_future.result()

    prompt = build_prompt(context, user_question)

    answer = local_llm_generate(prompt)

    return answer.strip()