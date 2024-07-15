from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import cast, String
import httpx
import uuid
from app.core.db import get_db
from app.models.pokemon import Pokemon

router = APIRouter()

"""
Function to fetch and seed the Pokeman data to Database  
"""
async def fetch_and_store_pokemons(db: AsyncSession):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://pokeapi.co/api/v2/pokemon?limit=10")
        pokemons = response.json()["results"]

        for pokemon in pokemons:
            poke_response = await client.get(pokemon["url"])
            poke_data = poke_response.json()
            types = [t["type"]["name"] for t in poke_data["types"]]
            new_pokemon = Pokemon(
                id=poke_data["id"],
                name=poke_data["name"],
                image=poke_data["sprites"]["front_default"],
                types=types,
            )
            db.add(new_pokemon)
        await db.commit()

@router.post("/fetch_pokemons")
async def fetch_pokemons(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pokemon).limit(1))
    pokemon_exists = result.scalar() is not None

    if pokemon_exists:
        return {"message": "Pokemon data already present"}
    
    await fetch_and_store_pokemons(db)
    return {"message": "Pokemon data fetched and stored successfully"}

@router.get("/pokemons")
async def get_pokemons(name: str = "", type: str = "", db: AsyncSession = Depends(get_db)):
    query = select(Pokemon)
    if name:
        query = query.where(Pokemon.name.ilike(f"%{name}%"))
    if type:
        query = query.where(cast(Pokemon.types, String).like(f"%{type}%"))
    result = await db.execute(query)
    pokemons = result.scalars().all()
    return pokemons

from sqlalchemy import text
@router.delete("/pokemons")
async def delete_all_pokemons(db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            stmt = text("TRUNCATE TABLE pokemons RESTART IDENTITY;")
            await db.execute(stmt)
            await db.commit()
        return {"message": "All pokemons deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete pokemons: {str(e)}")