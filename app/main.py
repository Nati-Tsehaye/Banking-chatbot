from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uuid
from .config import MODEL_PATH, VECTORIZER_PATH, MAPPINGS_PATH
from .chatbot import ChatbotService

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize chatbot
chatbot = ChatbotService(MODEL_PATH, VECTORIZER_PATH, MAPPINGS_PATH)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    
    try:
        while True:
            data = await websocket.receive_text()
            response = chatbot.generate_response(data, session_id)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print(f"Client disconnected: {session_id}")