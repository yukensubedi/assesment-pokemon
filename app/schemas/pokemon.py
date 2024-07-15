from pydantic import BaseModel
from typing import List

class PokemonCreate(BaseModel):
    id: int
    name: str
    image: str
    types: List[str]

    class Config:
        form_attributes = True

