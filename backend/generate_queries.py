# backend/generate_queries.py

def generate_safe_queries(metadata: dict) -> list[str]:
    queries = []
    if metadata.get("procedure_codes"):
        codes = " ".join(metadata["procedure_codes"])
        queries.append(f"X12 837 procedure code rules for {codes}")
    if metadata.get("diagnosis_codes"):
        diags = " ".join(metadata["diagnosis_codes"])
        queries.append(f"ICD-10 diagnosis codes {diags} meaning and guidelines")
    if metadata.get("total_charge") is not None:
        queries.append("837 total charge interpretation")
    if metadata.get("service_line_count", 0) > 0:
        queries.append(f"837 service line structure and rules with {metadata['service_line_count']} lines")
    return queries