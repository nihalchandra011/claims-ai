from backend.web_search import ollama_web_search
from backend.llm_local import local_llm_generate
import concurrent.futures


def build_prompt(metadata: dict, user_question: str, search_context: str):

    context = ""

    if search_context:
        context = search_context[:600]

    if metadata:
        context += f"\nClaim Data: {metadata}"

    prompt = f"""
You are ClaimsAI, an expert healthcare claims and contracts analyst.

Explain concepts clearly like a senior healthcare data analyst mentoring a junior analyst.

Use:
- clear explanations
- bullet points
- examples when useful

Context:
{context}

Question:
{user_question}

Provide a clear explanation:
"""

    return prompt


def agent_answer(metadata: dict, user_question: str):

    safe_query = user_question

    if metadata.get("procedure_codes"):
        safe_query += " " + " ".join(metadata["procedure_codes"])

    # PARALLEL SEARCH
    with concurrent.futures.ThreadPoolExecutor() as executor:

        search_future = executor.submit(
            ollama_web_search,
            safe_query
        )

        search_context = search_future.result()

    prompt = build_prompt(metadata, user_question, search_context)

    answer = local_llm_generate(prompt)

    return answer