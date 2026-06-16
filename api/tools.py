def record_user_details(email, name="Name not provided", notes="not provided"):
    print(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}


def record_unknown_question(question):
    print(f"Recording {question}")
    return {"recorded": "ok"}


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
                    "notes": {"type": "string", "description": "Zusätzliche Notizen zum Nutzer"}
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