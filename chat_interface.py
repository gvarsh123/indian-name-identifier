import gradio as gr
import requests
import json
import logging
from typing import List, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_ollama_response(prompt: str) -> str:
    """Get response from Ollama API."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        logger.error(f"Error getting response from Ollama: {str(e)}")
        return f"Error: {str(e)}"

def format_chat_history(history: List[Tuple[str, str]]) -> str:
    """Format the chat history into a string for the model."""
    formatted = []
    for human, assistant in history:
        formatted.append(f"Human: {human}")
        formatted.append(f"Assistant: {assistant}")
    return "\n".join(formatted)

def chat_with_llm(message: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
    try:
        # Format the conversation history
        history_text = format_chat_history(history)
        prompt = f"{history_text}\nHuman: {message}\nAssistant:"
        
        # Get response from Ollama
        response = get_ollama_response(prompt)
        
        # Add the response to history
        history.append((message, response))
        
        return "", history
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        return "", history + [(message, f"Error: {str(e)}")]

# Create the Gradio interface
with gr.Blocks(title="Chat with Llama3.2") as demo:
    gr.Markdown("# Chat with Llama3.2")
    gr.Markdown("This is a simple chat interface connected to your local Llama3.2 model running on Ollama.")
    
    chatbot = gr.Chatbot(height=500)
    msg = gr.Textbox(label="Your message", placeholder="Type your message here...")
    clear = gr.Button("Clear")
    
    msg.submit(chat_with_llm, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    logger.info("Starting Gradio interface...")
    demo.launch() 