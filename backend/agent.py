from backend.router import classify_question
from backend.llm_local import local_llm_generate
from backend.tools.tool_registry import TOOLS


def build_prompt(context, question):

    prompt = f"""
You are ClaimsAI, a healthcare claims and contracts expert.

Use the provided context to answer the question clearly.

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt


def agent_answer(metadata: dict, question: str):

    route = classify_question(question)

    context = ""

    if route == "web_search":

        tool = TOOLS["web_search"]
        context = tool(question)

    elif route == "claim_tool":

        tool = TOOLS["claim_parser"]
        context = tool(metadata)

    elif route == "contract_tool":

        tool = TOOLS["contract_parser"]
        context = tool(metadata)

    prompt = build_prompt(context, question)

    answer = local_llm_generate(prompt)

    return answer.strip()