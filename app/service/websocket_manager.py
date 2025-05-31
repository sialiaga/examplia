# your_fastapi_project/services/websocket_manager.py

from typing import Dict, Optional # Importa Optional para el nuevo método
from fastapi import WebSocket, WebSocketDisconnect

class WebSocketManager:
    def __init__(self):
        self.active_websockets: Dict[str, WebSocket] = {}
        print("WebSocketManager inicializado con diccionario de conexiones.")

    async def is_connect(self, connection_id: str):
        return connection_id in self.active_websockets
    
    async def connect(self, websocket: WebSocket, connection_id: str):
        await websocket.accept()
        self.active_websockets[connection_id] = websocket
        print(f"Nuevo cliente conectado: {connection_id}. Conexiones activas: {len(self.active_websockets)}")

    async def disconnect(self, connection_id: str):
        if connection_id in self.active_websockets:
            del self.active_websockets[connection_id]
            print(f"Cliente desconectado: {connection_id}. Conexiones activas: {len(self.active_websockets)}")
        else:
            print(f"Intento de desconectar ID no existente: {connection_id}")


    async def send_personal_message(self, message: str, connection_id: str) -> bool:
        """
        Envía un mensaje a un cliente WebSocket específico por su ID.
        Retorna True si el mensaje fue enviado exitosamente, False de lo contrario.
        """
        websocket = self.active_websockets.get(connection_id)
        if websocket:
            try:
                await websocket.send_text(message)
                print(f"Mensaje enviado a {connection_id}: {message}")
                return True
            except RuntimeError as e:
                print(f"Error al enviar a WebSocket {connection_id} (probablemente cerrado): {e}")
                # Si hay un error al enviar, asumimos que la conexión ya no es válida y la eliminamos
                if connection_id in self.active_websockets:
                    del self.active_websockets[connection_id]
                return False
            except Exception as e:
                print(f"Error desconocido al enviar a WebSocket {connection_id}: {e}")
                if connection_id in self.active_websockets:
                    del self.active_websockets[connection_id]
                return False
        else:
            print(f"No se encontró WebSocket para el ID: {connection_id}")
            return False

    async def broadcast(self, message: str) -> int:
        """Envía un mensaje a todos los clientes WebSocket conectados."""
        print(f"Enviando broadcast a {len(self.active_websockets)} clientes.")
        sent_count = 0
        for connection_id in list(self.active_websockets.keys()):
            if await self.send_personal_message(message, connection_id):
                sent_count += 1
        return sent_count

websocket_manager: WebSocketManager = WebSocketManager()