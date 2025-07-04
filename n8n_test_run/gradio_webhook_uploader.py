import gradio as gr
import requests

WEBHOOK_URL = "http://localhost:5678/webhook/04e1eb4e-0d78-4fb8-b72c-2125ed17da20"  # Update this if your webhook URL is different
CHAT_WEBHOOK_URL = "http://localhost:5678/webhook/cd9924cf-cdfd-4833-8d88-684dfb6249e2"

def send_to_webhook(website_text):
    # Show loading in Gradio automatically, no need for gr.Progress context
    try:
        response = requests.post(WEBHOOK_URL, json={"text": website_text}, timeout=60)
        response.raise_for_status()
        return "Upload complete!"
    except Exception as e:
        return f"Error: {str(e)}"

def chat_with_agent(message, history):
    try:
        # Optionally, send the full history for context
        payload = {"question": message, "history": history}
        response = requests.post(CHAT_WEBHOOK_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        # Filter for 'output' key if present, else fallback to 'reply', 'answer', or str(data)
        reply = data.get("output") or data.get("reply") or data.get("answer") or str(data)
        # If reply is a dict, fallback to str
        if isinstance(reply, dict):
            reply = str(reply)
        history = history + [[message, reply]]
        return "", history
    except Exception as e:
        reply = f"Error: {str(e)}"
        history = history + [[message, reply]]
        return "", history

with gr.Blocks() as demo:
    gr.Markdown("# Website Text Uploader and Agent Chat")
    with gr.Row():
        with gr.Column():
            gr.Markdown("## Upload Website Text")
            text_input = gr.Textbox(label="Paste website text here", lines=10, placeholder="Paste website content...")
            upload_output = gr.Textbox(label="Status")
            upload_btn = gr.Button("Upload to Webhook")
            upload_btn.click(send_to_webhook, inputs=text_input, outputs=upload_output)
    gr.Markdown("---")
    with gr.Row():
        with gr.Column():
            gr.Markdown("## Chat with Agent")
            chatbot = gr.Chatbot(label="Agent Chat")
            chat_input = gr.Textbox(label="Your message", placeholder="Type your question and press Enter...")
            send_btn = gr.Button("Send")
            def user_submit(msg, history):
                return "", history + [[msg, None]]
            chat_input.submit(user_submit, [chat_input, chatbot], [chat_input, chatbot], queue=False).then(
                chat_with_agent, [chat_input, chatbot], [chat_input, chatbot]
            )
            send_btn.click(user_submit, [chat_input, chatbot], [chat_input, chatbot], queue=False).then(
                chat_with_agent, [chat_input, chatbot], [chat_input, chatbot]
            )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, show_error=True)
