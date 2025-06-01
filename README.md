# Examplia

## Comandos importantes

### Instalación de dependencias

```bash
cd app
pip install -r requirements.txt
```
 
### Comando para poblar la tabla de objetivos de aprendizaje (OAs) con los del curriculum nacional

```bash
python app\scripts\import_oas.py --file app\uploadable_files\oas.xlsx
```

### Comando para comenzar la api en local

```bash
python -m uvicorn app.main:app --reload
```

## Endpoints

La API de Examplia ofrece los siguientes endpoints:

### Lecciones (Lessons)

- `GET /lessons/` - Listar todas las lecciones
- `POST /lessons/` - Crear una nueva lección
- `GET /lessons/{lesson_id}/oas` - Obtener los OAs asociados a una lección
- `POST /lessons/{lesson_id}/upload-slide` - Subir un archivo PDF o PPTX para una lección

### Objetivos de Aprendizaje (OAs)

- `GET /lessons/oas/` - Listar todos los OAs
- `POST /lessons/oa/` - Crear un nuevo OA
- `GET /lessons/oa/{oa_id}/lessons` - Obtener las lecciones asociadas a un OA

### Asociaciones

- `POST /lessons/oas` - Asociar un OA con una lección

### Telegram / WebSockets

- `POST /handshake/` - Verificar conexión de usuario
- `POST /instruction/` - Enviar instrucciones (explain/move) a un usuario conectado
