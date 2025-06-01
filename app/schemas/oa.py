from pydantic import BaseModel
from uuid import UUID

class OABase(BaseModel):
    curso: str
    asignatura: str
    unidad: str
    codigo: str
    description: str

class OACreate(OABase):
    pass

class OAOut(OABase):
    id: UUID

    model_config = {
        "from_attributes": True
    }
