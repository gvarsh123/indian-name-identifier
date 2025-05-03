from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Indian Name Identifier API",
    description="API for identifying Indian origin names using Llama 3.2 model",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NameRequest(BaseModel):
    name: str

class NameResponse(BaseModel):
    is_indian: int

@app.post("/api/identify-name", response_model=NameResponse)
async def identify_name(request: NameRequest):
    """
    Identify if a name is of Indian origin.
    
    - **name**: The name to be identified
    - **returns**: 1 if the name is identified as Indian origin, 0 otherwise
    """
    try:
        # Create the prompt with specific instructions
        prompt = f"""You are a Indian origin name identifier. Return 1 if the name you identify as Indian Origin, return 0 otherwise. Do not return any logic or explanation.
Name: {request.name}
Answer:"""
        
        logger.info(f"Sending name identification request to Ollama: {request.name}")
        
        # Get response from Ollama
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
            
        # Extract the numeric response
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
    uvicorn.run(app, host="0.0.0.0", port=8001) 