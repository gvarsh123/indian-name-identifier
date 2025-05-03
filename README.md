# LocalChatGPT

A modern chat interface that connects to your local Llama 3.2 model running on Ollama.

## Features

- Beautiful and responsive UI with Tailwind CSS
- Real-time chat interface
- Preserves conversation history
- Multiple chat sessions
- Clear button to start new conversations
- Error handling and logging
- FastAPI backend with CORS support

## Prerequisites

- Python 3.8 or higher
- Node.js and npm
- Ollama running locally with Llama 3.2 model
- pip (Python package manager)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/gvarsh123/LocalChatGPT.git
cd LocalChatGPT
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

## Usage

1. Start the backend server:
```bash
python backend.py
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

3. Open your web browser and navigate to http://localhost:5173

4. Start chatting with your local Llama 3.2 model!

## Project Structure

```
LocalChatGPT/
├── backend.py          # FastAPI backend server
├── requirements.txt    # Python dependencies
├── frontend/          # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── App.tsx     # Main application
│   │   └── main.tsx    # Entry point
│   └── package.json    # Node.js dependencies
└── README.md          # This file
```

## API Documentation

The backend provides a REST API for chat interactions:

### POST /api/chat

Send a message to the model and get a response.

**Request Body:**
```json
{
    "message": "string",
    "session_id": "string"
}
```

**Response:**
```json
{
    "response": "string",
    "session_id": "string"
}
```

## License

MIT 