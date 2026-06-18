import requests
from api.config import N8N_WEBHOOK_URL, N8N_WEBHOOK_SECRET
from pydantic import BaseModel, EmailStr, ValidationError

class UserDetails(BaseModel):
    email: EmailStr
    name: str = "Name not provided"
    notes: str = "not provided"

def _trigger_webhook(payload: dict):
    headers = {"X-CV-Bot-Secret": N8N_WEBHOOK_SECRET}
    try:
        resp = requests.post(N8N_WEBHOOK_URL, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Webhook failed: {e}")
        return False
    return True


def record_user_details(email, name="Name not provided", notes="not provided"):
    try:
        data = UserDetails(email=email, name=name, notes=notes)
    except ValidationError as e:
        print(f"Validation failed: {e}")
        return {"recorded": "invalid", "error": str(e)}

    print(f"Recording {data.name} with email {data.email}")
    ok = _trigger_webhook({"type": "user_details", **data.model_dump()})
    return {"recorded": "ok" if ok else "failed"}


def record_unknown_question(question):
    print(f"Recording {question}")
    ok = _trigger_webhook({
        "type": "unknown_question",
        "question": question,
    })
    return {"recorded": "ok" if ok else "failed"}

tools = [
    {
        "type": "function",
        "function": {
            "name": "record_user_details",
            "description": "Speichert die Kontaktdaten eines Nutzers, der Interesse zeigt oder Kontakt aufnehmen möchte.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "E-Mail-Adresse des Nutzers"},
                    "name": {"type": "string", "description": "Name des Nutzers"},
                    "notes": {"type": "string", "description": "Eine kurze Zusammenfassung des Chats des Nutzers, insbesondere im Hinblick darauf, für welche Technologien und Dienstleistungen sich der Nutzer interessiert. Falls der Nutzer bereits eine Projektidee im Chat formuliert hat, diese hier auch ausführlich zusammengefasst eintragen."}
                },
                "required": ["email"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_unknown_question",
            "description": "Speichert eine Frage, die nicht beantwortet werden konnte.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "Die unbeantwortete Frage"}
                },
                "required": ["question"]
            }
        }
    }
]

tool_map = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}