from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import logging
from typing import List, Tuple, Optional, Dict
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Name Identifier API",
    description="API for identifying Indian origin names using Llama 3.2 model",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# In-memory storage for chat sessions
chat_sessions: Dict[str, List[Tuple[str, str]]] = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    response: str
    session_id: str

# New name identifier model
class NameRequest(BaseModel):
    name: str

class NameResponse(BaseModel):
    is_indian: int

def format_chat_history(history: List[Tuple[str, str]]) -> str:
    """Format the chat history into a string for the model."""
    if not history:
        return ""
    formatted = []
    for human, assistant in history:
        formatted.append(f"Human: {human}")
        formatted.append(f"Assistant: {assistant}")
    return "\n".join(formatted)

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        logger.info(f"Received chat request: {request}")
        
        # Get or create session
        if request.session_id not in chat_sessions:
            chat_sessions[request.session_id] = []
            logger.info(f"Created new session: {request.session_id}")
        
        history = chat_sessions[request.session_id]
        history_text = format_chat_history(history)
        prompt = f"{history_text}\nHuman: {request.message}\nAssistant:"
        
        logger.info(f"Sending prompt to Ollama: {prompt}")
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        response.raise_for_status()
        
        response_data = response.json()
        if "response" not in response_data:
            raise ValueError("Invalid response format from Ollama")
            
        # Update session history
        chat_sessions[request.session_id].append((request.message, response_data["response"]))
        
        return ChatResponse(
            response=response_data["response"],
            session_id=request.session_id
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error: {str(e)}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except ValueError as e:
        logger.error(f"Invalid response format: {str(e)}")
        raise HTTPException(status_code=500, detail="Invalid response from model")
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/identify-name", response_model=NameResponse)
async def identify_name(request: NameRequest):
    """
    Identify if a name is of Indian origin.
    
    - **name**: The name to be identified
    - **returns**: 1 if the name is identified as Indian origin, 0 otherwise
    """
    try:
        prompt = f"""You are a Indian origin name identifier. Return 1 if the name you identify as Indian Origin, return 0 otherwise. Do not return any logic or explanation.
Name: {request.name}
Answer:"""
        
        logger.info(f"Sending name identification request to Ollama: {request.name}")
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        response.raise_for_status()
        
        response_data = response.json()
        if "response" not in response_data:
            raise ValueError("Invalid response format from Ollama")
            
        try:
            is_indian = int(response_data["response"].strip())
            if is_indian not in [0, 1]:
                raise ValueError("Response must be 0 or 1")
        except ValueError:
            raise ValueError("Invalid response format: expected 0 or 1")
            
        return NameResponse(is_indian=is_indian)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error: {str(e)}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except ValueError as e:
        logger.error(f"Invalid response format: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error in name identification: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 