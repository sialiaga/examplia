# your_fastapi_project/services/websocket_manager.py

from typing import Dict, Any, Optional # Importa Any para el tipo de lesson_id
from fastapi import WebSocket, WebSocketDisconnect

class WebSocketManager:
    def __init__(self):
        self.active_websockets: Dict[str, Dict[str, Any]] = {}
        print("WebSocketManager inicializado con diccionario de conexiones y datos adicionales.")

    async def is_connect(self, connection_id: str) -> bool:
        """
        Verifica si un cliente con el ID de conexión dado está actualmente conectado.
        """

        return connection_id in self.active_websockets

    async def connect(self, websocket: WebSocket, lesson_id: Any, connection_id: str):
        """
        Acepta una nueva conexión WebSocket y la almacena con su ID de conexión y de lección.
        """
        await websocket.accept()
        # Almacenamos un diccionario que contiene el objeto WebSocket y el lesson_id asociado
        self.active_websockets[connection_id] = {"websocket": websocket, "lesson_id": lesson_id}
        print(self.active_websockets)
        print(f"Nuevo cliente conectado: {connection_id} (Lección: {lesson_id}). Conexiones activas: {len(self.active_websockets)}")

    async def disconnect(self, connection_id: str):
        """
        Desconecta y elimina un cliente WebSocket de la lista de conexiones activas.
        """
        if connection_id in self.active_websockets:
            del self.active_websockets[connection_id]
            print(f"Cliente desconectado: {connection_id}. Conexiones activas: {len(self.active_websockets)}")
        else:
            print(f"Intento de desconectar ID no existente: {connection_id}")


    async def _send_message_to_single_socket(self, message: str, connection_id: str) -> bool:
        """
        Función auxiliar interna para enviar un mensaje a un solo WebSocket
        y manejar la limpieza si falla.
        Retorna True si el mensaje fue enviado, False de lo contrario.
        """
        connection_data = self.active_websockets.get(connection_id)
        if connection_data and "websocket" in connection_data:
            websocket = connection_data["websocket"]
            try:
                await websocket.send_text(message)
                print(f"Mensaje enviado a {connection_id}: {message}") # Descomenta para más logs
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

    async def send_personal_message(self, message: str, connection_id: str) -> bool:
        """
        Envía un mensaje a un cliente WebSocket específico por su ID de conexión.
        """
        return await self._send_message_to_single_socket(message, connection_id)


    async def broadcast(self, message: str) -> int:
        """
        Envía un mensaje a todos los clientes WebSocket conectados.
        """
        print(f"Enviando broadcast a {len(self.active_websockets)} clientes.")
        sent_count = 0
        # Itera sobre una copia de las claves para poder modificar el diccionario durante la iteración
        for connection_id in list(self.active_websockets.keys()):
            if await self._send_message_to_single_socket(message, connection_id):
                sent_count += 1
        return sent_count

websocket_manager = WebSocketManager()