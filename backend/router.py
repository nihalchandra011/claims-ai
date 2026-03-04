def classify_question(question: str):

    q = question.lower()

    # healthcare claim logic
    claim_keywords = [
        "837",
        "835",
        "claim",
        "encounter",
        "edi",
        "x12",
        "payer",
        "remittance"
    ]

    error_keywords = [
        "error",
        "reject",
        "denial",
        "denied",
        "a7",
        "eob"
    ]

    contract_keywords = [
        "contract",
        "agreement",
        "clause",
        "reimbursement",
        "terms"
    ]

    for k in claim_keywords:
        if k in q:
            return "claims"

    for k in error_keywords:
        if k in q:
            return "errors"

    for k in contract_keywords:
        if k in q:
            return "contract"

    return "general"