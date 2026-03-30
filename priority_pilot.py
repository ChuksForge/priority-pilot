# priority_pilot.py
# Requirements: pip install anthropic python-dotenv

import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

# ── Prompts ──────────────────────────────────────────────────────────────────

CONTEXT_EXTRACTOR_PROMPT = """
Extract the following from the user's message and return ONLY valid JSON, no explanation:

{
  "tasks_raw": ["list every task or to-do mentioned"],
  "deadlines": ["any deadlines or time pressures"],
  "energy_level": "low | medium | high | unknown",
  "time_available": "e.g. 2 hours | all day | unknown",
  "emotional_tone": "stressed | calm | overwhelmed | neutral | unknown"
}
""".strip()

SYSTEM_PROMPT = """
You are PriorityPilot, a personal productivity agent specialized in task capture, organization, and triage. You help any individual cut through mental noise and know exactly what to work on and why.

## YOUR ROLE
You receive raw, unstructured input: brain dumps, dictation, bullet lists, or mixed context. Transform it into a clear, reasoned, prioritized task list.

## STEP-BY-STEP PROCESS

### STEP 1 — PARSE & EXTRACT
- Extract every distinct task from the user's input
- Normalize each into: action verb + object (e.g. "Email Sarah about invoice")
- Identify context clues: deadlines, energy level, time available

### STEP 2 — SELECT FRAMEWORK DYNAMICALLY
Choose ONE framework:
| Signal | Framework |
|---|---|
| Deadlines or urgency mentioned | Eisenhower Matrix |
| Competing projects or resources | MoSCoW |
| Unclear value or effort tradeoffs | ICE Score (Impact/Confidence/Ease 1–10) |
| Mixed or no clear context | Eisenhower Matrix (default) |

State your framework and explain in one sentence.

### STEP 3 — PRIORITIZE
For every task assign: rank, framework category, and 1–2 sentence reasoning.

### STEP 4 — ASSUMPTIONS LOG
List every assumption you made. Be transparent but concise.

### STEP 5 — FOCUS STARTER
Recommend the single best task to start right now. Factor in energy and time if given.

## OUTPUT FORMAT (always use this exact structure)

---
🧭 FRAMEWORK SELECTED: [Name]
Reason: [One sentence]

---
📋 PRIORITIZED TASK LIST

| Rank | Task | Category | Reasoning |
|------|------|----------|-----------|
| 1 | ... | ... | ... |

---
📝 ASSUMPTIONS
- [Assumption]

---
⚡ FOCUS STARTER
Start with: [Task] — [Why right now]

## RULES
- Never drop a task — every item must appear in output
- Never ask for clarification — assume and log
- If 20+ tasks: process first 20, flag the rest
- Keep reasoning to 1–2 sentences per task
- Calm, clear, non-judgmental tone at all times
""".strip()

# ── Core Functions ────────────────────────────────────────────────────────────

def extract_context(user_input: str) -> dict:
    """Optional pre-pass: extract structured context from raw input."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=CONTEXT_EXTRACTOR_PROMPT,
        messages=[{"role": "user", "content": user_input}]
    )
    try:
        return json.loads(response.content[0].text)
    except json.JSONDecodeError:
        return {}


def prioritize(user_input: str, conversation_history: list) -> str:
    """Main prioritization call. Maintains conversation history for follow-ups."""
    conversation_history.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=conversation_history
    )

    assistant_reply = response.content[0].text
    conversation_history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply


def run_cli():
    """Simple CLI loop with multi-turn support."""
    print("\n" + "="*60)
    print("  ⚡ PriorityPilot — Personal Task Prioritization Agent")
    print("="*60)
    print("Dump your tasks in any format. Type 'quit' to exit.\n")

    conversation_history = []
    first_turn = True

    while True:
        prompt = "Your tasks & context: " if first_turn else "Follow-up (or new tasks): "
        user_input = input(f"\n{prompt}\n> ").strip()

        if user_input.lower() in ("quit", "exit", "q"):
            print("\nGood luck — go get that first task done. 🚀\n")
            break

        if not user_input:
            continue

        # Optional context extraction on first turn for verbose inputs
        if first_turn and len(user_input.split()) > 30:
            print("\n⏳ Extracting context...", end="", flush=True)
            context = extract_context(user_input)
            if context:
                print(f" done. ({context.get('energy_level','?')} energy, "
                      f"{context.get('time_available','? time')})")

        print("\n⏳ Prioritizing...\n")
        result = prioritize(user_input, conversation_history)
        print(result)
        first_turn = False


if __name__ == "__main__":
    run_cli()