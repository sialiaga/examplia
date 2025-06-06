# your_fastapi_project/api/websockets/router.py

import random 
import string
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status, Query
from ..service.websocket_manager import websocket_manager
from typing import Dict, Any, Optional
import json
import asyncio

websocket_router = APIRouter()


def generate_short_connection_id(length: int = 4) -> str:
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for i in range(length))

@websocket_router.websocket("/ws/{lesson_id}")
async def ws_connect(websocket: WebSocket, lesson_id: str):
    connection_id = generate_short_connection_id()
    print(f"Generando ID de conexión: {connection_id}") # Para depuración

    await websocket_manager.connect(websocket, lesson_id, connection_id)
    
    
    stop_event = asyncio.Event()

    try:
       await websocket.send_text(json.dumps({"accion": "auth", "contenido":connection_id}))
       await stop_event.wait() 

    except WebSocketDisconnect:

        print(f"Cliente {connection_id} (Lección: {lesson_id}) se desconectó.")
        await websocket_manager.disconnect(connection_id)
    
    except Exception as e:
        print(f"Error inesperado en WebSocket para {connection_id}: {e}")
        await websocket_manager.disconnect(connection_id)
