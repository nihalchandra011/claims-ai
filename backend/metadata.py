# backend/metadata.py

def extract_837_metadata(parsed_x12: dict) -> dict:
    meta = {
        "procedure_codes": [],
        "diagnosis_codes": [],
        "service_line_count": 0,
        "total_charge": None,
    }

    for seg in parsed_x12.get("segments", []):
        sid = seg.get("id")
        elems = seg.get("elements", [])

        if sid in ("SV1", "SV2"):
            if len(elems) > 1:
                meta["procedure_codes"].append(elems[1])

        if sid == "HI":
            for e in elems:
                if ":" in e:
                    _, code = e.split(":")
                    meta["diagnosis_codes"].append(code)

        if sid == "LX":
            meta["service_line_count"] += 1

        if sid == "CLM":
            try:
                meta["total_charge"] = float(elems[1])
            except Exception:
                pass

    meta["procedure_codes"] = list(set(meta["procedure_codes"]))
    meta["diagnosis_codes"] = list(set(meta["diagnosis_codes"]))
    return meta