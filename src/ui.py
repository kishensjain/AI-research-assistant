import gradio as gr
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url = "https://ollama.com/v1",
    api_key = os.getenv("OLLAMA_API_KEY")
)

MODEL = "gpt-oss:120b"

def build_ui() -> gr.Blocks:
    with gr.Blocks(title="AI research assistant") as demo:
        gr.Markdown("# 🔍 AI Research Assistant by Kishen\nLoad URLs or paste text, then ask questions about it.")

        chunks_state = gr.State([]) 

        with gr.Row():
            with gr.Column(scale=1):
                sources_input = gr.Textbox(
                    label="Sources",
                    placeholder="Enter one URL or text block per line...",
                    lines=5
                )
                file_input = gr.File(
                    label="Or upload PDF / Word files",
                    file_types=[".pdf", ".docx"],
                    file_count="multiple"
                )
                load_btn = gr.Button("Load Sources", variant="primary")
                load_output = gr.Textbox(label="Load Status", lines=5, interactive=False)

            with gr.Column(scale=2):
                chatbot = gr.Chatbot(label="Chat", height=450)
                user_input = gr.Textbox(
                    label="Your question",
                    placeholder="Ask something about your sources...",
                )
                send_btn = gr.Button("Send", variant="primary")
    return demo