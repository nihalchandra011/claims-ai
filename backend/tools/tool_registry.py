from backend.web_search import ollama_web_search


def run_web_search(query):

    try:
        results = ollama_web_search(query)

        if not results:
            return "No web results found."

        return results

    except Exception as e:
        return f"Search failed: {str(e)}"


def run_claim_parser(metadata):

    if not metadata:
        return "No claim metadata available."

    return f"Parsed claim metadata: {metadata}"


def run_contract_parser(text):

    if not text:
        return "No contract text detected."

    return f"Contract summary context: {text[:500]}"


TOOLS = {
    "web_search": run_web_search,
    "claim_parser": run_claim_parser,
    "contract_parser": run_contract_parser
}