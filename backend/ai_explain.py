# backend/ai_explain.py

def explain_claim_issues(metadata: dict, search_results: list[str]) -> str:
    lines = ["Claim Summary:"]
    if not metadata["procedure_codes"]:
        lines.append("No procedure codes found.")
    else:
        lines.append(f"Procedure codes: {metadata['procedure_codes']}")
    if not metadata["diagnosis_codes"]:
        lines.append("No diagnosis codes found.")
    lines.append(f"Service lines: {metadata['service_line_count']}")
    if metadata["total_charge"] is not None:
        lines.append(f"Total charge: {metadata['total_charge']}")
    for sr in search_results:
        lines.append("Context from search: " + (sr[:300] + "..."))
    return "\n".join(lines)