from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv

app = FastAPI()

#"BD" de prueba

contexto1 = """
Esty trabajando con estudiantes de segundo medio en una clase de química que aborda los estados de la materia, los cambios de estado y la importancia de entender conceptos como fusión, evaporación, condensación, solidificación y sublimación. 
El objetivo de la clase es que los estudiantes comprendan cómo la materia cambia de estado según la temperatura y la presión, y puedan identificar ejemplos cotidianos de estos fenómenos (por ejemplo, el derretimiento del hielo, la evaporación del agua al hervir, o la formación de escarcha).
También se busca desarrollar habilidades de pensamiento crítico, permitiéndoles relacionar estos conceptos con la vida diaria y la importancia de la energía en los cambios de estado.
Además, se fomenta el uso de ejemplos visuales (imágenes o diagramas) para ayudar a entender las transiciones de fase.
"""
contexto2 = """
 Estoy trabajando con estudiantes de segundo medio en una clase de biología, cuyo objetivo es comprender el proceso de la fotosíntesis en las plantas.
Durante la clase, se abordan conceptos como la energía lumínica, la transformación de materia inorgánica en orgánica, el rol de la clorofila y la producción de oxígeno como subproducto.
Los estudiantes deben relacionar estos procesos con su impacto en la vida cotidiana, como la importancia de las plantas en la producción de oxígeno y el ciclo del carbono.
Además, se busca que los estudiantes aprendan a interpretar diagramas de procesos biológicos, como esquemas de la fotosíntesis o el ciclo del carbono, para fortalecer su comprensión visual de los conceptos.
 """

CONTEXT_DB = {
    12345: {"contexto" : contexto1, "Transcripción":"Explícame cómo se producen los cambios de estado en la materia y su importancia en la vida cotidiana."},
    67891:{"contexto": contexto2 ,"Transcripción":"Podrías darme un ejemplo de fotosíntesis explicada con un diagrama? Quiero entender cómo la luz, el agua y el dióxido de carbono se transforman en glucosa y oxígeno."}
}

openai.api_key = os.environ.get("API-KEY")


class TranscriptionData(BaseModel):
    user_id: int
    text: str

@app.post("/transcription/")
async def receive_transcription(data: TranscriptionData):
    print(f"Recibí de usuario {data.user_id}: {data.text}")
    return {"status": "ok", "message": f"Transcripción recibida: {data.text}"}

if __name__ == "__main__":
    uvicorn.run("mock_api:app", host="127.0.0.1", port=8000, reload=True)
