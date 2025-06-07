from typing import Literal
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from ..service.websocket_manager import websocket_manager
import json

import requests
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

pixabay_apikey = os.getenv("PBKEY")



telegram = APIRouter()


def obtener_link_pixabay(texto_busqueda: str, api_key: str) -> str:
    print(pixabay_apikey)
    url_image_to_show = "https://i.pinimg.com/564x/85/f0/53/85f0533df9912c5bd700903a918930c8.jpg"
    
    api_url = "https://pixabay.com/api/"
    params = {
        'key': api_key,
        'q': texto_busqueda.split(),
        'lang': 'es'
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status() 

        data = response.json()

        if data['hits']:
            primera_foto = data['hits'][0]
            url_imagen = primera_foto['webformatURL']
            url_image_to_show = url_imagen
        else:
            print(f"No se encontraron fotos para '{texto_busqueda}' en Pixabay.")

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de Pixabay: {e}")
    
    except KeyError:
        print("La respuesta de la API de Pixabay no tiene el formato esperado.")

    return url_image_to_show


class authData(BaseModel):
    id: str

class InstructionMessage(BaseModel):
    id: str
    action: Literal["explain", "move"]
    desc: str


@telegram.post("/handshake/")
async def read_users(auth: authData):
    is_auth = await websocket_manager.is_connect(auth.id)
    if is_auth:
        return {"message": "User connected successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not connected or unauthorized"
        )
    
@telegram.post("/instruction/")
async def read_users(data: InstructionMessage):
    if not await websocket_manager.is_connect(data.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not connected or unauthorized."
        )

    response_payload = {"accion": data.action}

    if data.action == "explain":
        try:
            # TODO: Implement actual GPT API call here
            # For now, using a placeholder.
            # gpt_response = await call_gpt_api(data.desc)
            gpt_response = ["Example 1, fake text for example 1", "Example 2, fake text for example 2", "Example 3, fake text for example 3"]
            url_imagen = obtener_link_pixabay(data.desc, pixabay_apikey)

            response_payload["title"] = data.desc
            response_payload["contenido"] = gpt_response
            response_payload["image"] = url_imagen
        except Exception as e:
            # Log the error for debugging purposes
            print(f"Error calling GPT API: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get explanation from AI."
            )
    elif data.action == "move":
        if data.desc not in ["next", "prev"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid 'move' operation. 'desc' must be 'next' or 'prev'."
            )
        response_payload["contenido"] = data.desc

    await websocket_manager.send_personal_message(json.dumps(response_payload), data.id)

    return {"message": "Operation successfully"}
