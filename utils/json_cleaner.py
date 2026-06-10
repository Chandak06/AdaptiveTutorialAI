import json

def clean_json_response(text):

    text = text.replace("```json", "")
    text = text.replace("```", "")

    text = text.strip()

    return json.loads(text)