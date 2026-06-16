import json
from api.tools import tool_map, tools
from api.cv import get_cv_text
from api.prompts import system_prompt
from api.config import MAX_ROUNDS, MODEL, client

def execute_tools(tool_calls: dict):
    """Jeden Tool-Call ausführen und das Ergebnis als tool-Nachricht zurückgeben."""
    messages = []
    for tc in tool_calls.values():
        try:
            args = json.loads(tc["arguments"])
        except json.JSONDecodeError:
            args = {}
        fn = tool_map.get(tc["name"])
        result = fn(**args) if fn else {"error": "unknown tool"}
        messages.append({
            "role": "tool",
            "tool_call_id": tc["id"],
            "content": json.dumps(result),
        })
    return messages

def accumulate_tool_calls(tool_calls_dict, delta_tool_calls):
    """Tool-Calls kommen gestückelt an; hier kleben wir die Stücke zusammen."""
    for tc in delta_tool_calls:
        slot = tool_calls_dict.setdefault(
            tc.index, {"id": "", "name": "", "arguments": ""}
        )
        if tc.id:
            slot["id"] = tc.id
        if tc.function.name:
            slot["name"] = tc.function.name
        if tc.function.arguments:
            slot["arguments"] += tc.function.arguments


def build_assistant_message(content, tool_calls):
    """Die Assistant-Nachricht, die festhält, welche Tools das Modell wollte."""
    return {
        "role": "assistant",
        "content": content or None,
        "tool_calls": [
            {
                "id": tc["id"],
                "type": "function",
                "function": {"name": tc["name"], "arguments": tc["arguments"]},
            }
            for tc in tool_calls.values()
        ],
    }

def run_chat(messages):
    full_system = system_prompt + "\n\nLebenslauf:\n" + get_cv_text()
    msgs = [{"role": "system", "content": full_system}] + messages

    for _ in range(MAX_ROUNDS):
        stream = client.chat.completions.create(
            model=MODEL,
            stream=True,
            messages=msgs,
            tools=tools,
        )

        content = ""
        tool_calls_dict = {}

        # Eine Runde streamen: Text sofort durchreichen, Tool-Calls sammeln.
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                content += delta.content
                yield delta.content
            if delta.tool_calls:
                accumulate_tool_calls(tool_calls_dict, delta.tool_calls)

        # Keine Tools angefordert -> Antwort ist fertig.
        if not tool_calls_dict:
            break

        # Tools ausführen, Ergebnisse an die History hängen, nächste Runde.
        msgs.append(build_assistant_message(content, tool_calls_dict))
        msgs.extend(execute_tools(tool_calls_dict))



