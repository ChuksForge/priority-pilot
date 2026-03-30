# ui.py
import gradio as gr
from priority_pilot import prioritize, extract_context

conversation_history = []

def chat(user_input, history):
    global conversation_history

    if not user_input.strip():
        return "", history

    # Optional context extraction on first turn
    if not conversation_history and len(user_input.split()) > 30:
        extract_context(user_input)

    # Get response using Anthropic-format history
    result = prioritize(user_input, conversation_history)

    # Gradio 6.x format
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": result})

    return "", history

def reset():
    global conversation_history
    conversation_history = []
    return "", []

with gr.Blocks(title="PriorityPilot") as demo:
    gr.Markdown("# ⚡ PriorityPilot\n### Dump your tasks. Get a prioritized plan.")

    chatbot = gr.Chatbot(height=500, show_label=False)

    msg = gr.Textbox(
        placeholder="Brain dump your tasks here — any format, any mess...",
        label="Your input",
        lines=4
    )
    with gr.Row():
        submit = gr.Button("Prioritize →", variant="primary")
        clear = gr.Button("New Session")

    submit.click(chat, [msg, chatbot], [msg, chatbot])
    msg.submit(chat, [msg, chatbot], [msg, chatbot])
    clear.click(reset, outputs=[msg, chatbot])

demo.launch(theme=gr.themes.Soft())