# server/app/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import asyncio
import os

app = FastAPI(title="WS Docker Practice")

# Servir archivos estáticos (index.html)
app.mount("/static", StaticFiles(directory="static"), name="static")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception:
                # si falla, desconectar
                self.disconnect(connection)

manager = ConnectionManager()

@app.get("/")
async def root():
    return HTMLResponse(open("static/index.html", "r", encoding="utf-8").read())

# Endpoint WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await manager.send_personal_message("Conexión establecida. Envía mensajes.", websocket)
        while True:
            data = await websocket.receive_text()
            # Ejemplo simple: eco y broadcast del mensaje
            sender_msg = f"[ECO] {data}"
            await manager.send_personal_message(sender_msg, websocket)
            # opcional: reenviar a todos los demás
            await manager.broadcast(f"[BROADCAST] {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        manager.disconnect(websocket)

# Salud básica
@app.get("/health")
async def health():
    return {"status": "ok", "env": dict(os.environ)}
