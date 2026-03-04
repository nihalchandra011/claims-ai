import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"


def local_llm_generate(prompt: str):

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_predict": 400,      # allow longer answers
            "temperature": 0.3,
            "top_p": 0.9
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        stream=True,
        timeout=300
    )

    response.raise_for_status()

    final_text = ""

    for line in response.iter_lines():

        if not line:
            continue

        try:
            data = json.loads(line.decode("utf-8"))

            if "response" in data:
                token = data["response"]
                final_text += token

        except:
            pass

    # cleanup
    final_text = final_text.replace("Answer:", "").strip()

    return final_text