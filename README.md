# Pokemon API

## Setup Instructions



1. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows `venv\Scripts\activate`
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Setup PostgreSQL database and configure `.env` file:
    ```
    DATABASE_URL=postgresql+asyncpg://{user}:{password}@{hostname}:{port}/{database-name}
    ```

4. Run migrations to create database schema:
   
    ```bash
    alembic upgrade head
    ```
    

5. Start the API server:
    ```bash
    uvicorn app.main:app --reload
    ```

## API Documentation

Access the API documentation and interact with the endpoints using Swagger UI.
- [Swagger UI - http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

- `POST /api/v1/fetch_pokemons/`: Fetch and store Pokemon data from PokeAPI into the database.
- `GET /api/v1/pokemons/`: Get list of pokemons with optional `name` and `type` filters.




