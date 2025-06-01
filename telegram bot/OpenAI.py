import openai
import io
import matplotlib.pyplot as plt
import base64
import ast
import os
from dotenv import load_dotenv

load_dotenv()

# Cliente OpenAI v1.x.x
client = openai.OpenAI(api_key=os.environ.get("API-KEY"))


# System Profile actualizado para triples comillas
SYSTEM_PROFILE = """
Eres un bot llamado Examplia especializado en la generación de ejemplos en tiempo real para ayudar a profesores a resolver dudas de sus estudiantes.
Estas dudas se te entregarán junto con un contexto de la clase, y tu tarea es dar 3 ejemplos diferentes, cada uno acompañado de un diagrama que resuelva la duda del estudiante.
Responde SIEMPRE en formato JSON, y asegúrate de usar triple comillas (\"\"\") alrededor del código Python para cada valor de la clave 'Diagrama'. La estructura es:

{
    "Ejemplo1": {
        "Encabezado": "Una breve introducción explicando el concepto",
        "Diagrama": \"\"\"Código en Python usando matplotlib para crear el diagrama\"\"\"
    },
    "Ejemplo2": {
        "Encabezado": "...",
        "Diagrama": \"\"\"...\"\"\"
    },
    "Ejemplo3": {
        "Encabezado": "...",
        "Diagrama": \"\"\"...\"\"\"
    }
}

No incluyas explicaciones fuera del JSON.
"""

def obtener_respuesta_estructurada(concepto, contexto_clase):
    respuesta = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROFILE},
            {"role": "user", "content": f"Contexto de la clase: {contexto_clase}"},
            {"role": "user", "content": f"Pregunta del estudiante: {concepto}"}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    return respuesta.choices[0].message.content

def ejecutar_y_guardar_diagrama(codigo, output_path):
    try:
        codigo_modificado = codigo.replace("plt.show()", f"plt.savefig('{output_path}')\nplt.close()")
        local_vars = {}
        exec(codigo_modificado, {"plt": plt, "io": io, "os": os}, local_vars)
        print(f"✅ Diagrama guardado en {output_path}")
    except Exception as e:
        print("❌ Error al ejecutar el diagrama:", e)

if __name__ == "__main__":
    concepto = "¿Cómo es el diagrama de fuerzas en un cuerpo apoyado en un plano inclinado?"
    contexto_clase = "Clase de Física para estudiantes de secundaria sobre las fuerzas que actúan sobre un cuerpo en reposo o en movimiento en un plano inclinado (ángulo, peso, normal, rozamiento, etc.)."

    respuesta = obtener_respuesta_estructurada(concepto, contexto_clase)
    print("\nRespuesta completa del bot:\n")
    print(respuesta)

    # Parsear JSON
    try:
        data = ast.literal_eval(respuesta)

        output_dir = "diagrams"
        os.makedirs(output_dir, exist_ok=True)

        for key, value in data.items():
            encabezado = value.get("Encabezado", "")
            codigo_diagrama = value.get("Diagrama", "")

            print(f"\n===============================")
            print(f"🔎 {key}: {encabezado}")
            print(f"\n🔎 Código del diagrama para {key}:\n")
            print(codigo_diagrama)

            diagrama_path = os.path.join(output_dir, f"{key}_diagrama.png")
            ejecutar_y_guardar_diagrama(codigo_diagrama, diagrama_path)

    except Exception as e:
        print("❌ Error al procesar la respuesta JSON:", e)
