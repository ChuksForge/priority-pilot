# ⚡ PriorityPilot

A personal productivity AI agent that transforms messy task lists, brain dumps, 
and rambling dictation into a clear, reasoned, prioritized action plan.

Built with Claude (Anthropic) · Python · Optional Gradio UI

---

## What It Does

Most productivity tools make you do the organizing. PriorityPilot does it for you.

Give it anything — a chaotic brain dump, a voice note transcription, a bullet list — 
and it will:

- Extract every task, no matter how buried
- Dynamically select the best prioritization framework for your context
- Rank every task with clear, transparent reasoning
- Log every assumption it makes
- Tell you exactly what to start with right now

---

## Frameworks Used (auto-selected)

| Your Context | Framework Applied |
|---|---|
| Deadlines or urgency mentioned | Eisenhower Matrix (Urgent/Important) |
| Competing projects | MoSCoW (Must/Should/Could/Won't) |
| Ambiguous value or effort | ICE Score (Impact · Confidence · Ease) |
| No clear signals | Eisenhower Matrix (default) |

---

## Quickstart
```bash
git clone https://github.com/yourname/priority-pilot
cd priority-pilot
pip install -r requirements.txt
```

Add your API key:
```bash
echo "ANTHROPIC_API_KEY=sk-your-key-here" > .env
```

Run CLI:
```bash
python priority_pilot.py
```

Run with UI:
```bash
python ui.py
```

---

## Example Input → Output

**Input:**
```
finish the report by EOD, there's a prod bug affecting users, 
reply to client email, call mum, exercise. medium energy, 3 hours.
```

**Output:**
```
🧭 FRAMEWORK SELECTED: Eisenhower Matrix
Reason: Clear urgency signals make urgent/important sorting most effective.

📋 PRIORITIZED TASK LIST
| Rank | Task | Category | Reasoning |
| 1 | Fix production bug | Urgent & Important | Actively impacting users — highest cost. |
| 2 | Finish manager report | Urgent & Important | Hard EOD deadline, direct accountability. |
...

⚡ FOCUS STARTER
Start with: Fix production bug — highest leverage with 3 hours of medium energy.
```

---

## Multi-Turn Support

After the first prioritization, you can follow up:
- *"Why is X ranked above Y?"*
- *"I finished task 2, re-rank the rest"*
- *"Add two more tasks: ..."*
- *"I only have 30 minutes now"*

The agent maintains conversation context across the session.

---

## Project Structure
```
priority-pilot/
├── priority_pilot.py   # Core agent (CLI + logic)
├── ui.py               # Gradio web UI
├── demo
├── requirements.txt
└── README.md
```

---

## Design Decisions

- **Dynamic framework selection** — no hardcoded framework; the agent reads context signals and explains its choice
- **Two-prompt architecture** — a lightweight context extractor runs first on long inputs, keeping the main prompt clean
- **Assumptions log** — every gap is surfaced, not hidden; builds trust in the agent's output
- **Multi-turn conversation** — session history is maintained so users can refine, not restart

---

## Built With

- [Anthropic Claude API](https://anthropic.com)
- Python 3.10+
- Gradio (optional UI)

---

## Author

Built by **[ChuksForge]**

- Portfolio: chuksforge.github.io
- GitHub: [github.com/ChuksForge](https://github.com/ChuksForge)
- Email: chuksprompts@gmail.com

## License

MIT