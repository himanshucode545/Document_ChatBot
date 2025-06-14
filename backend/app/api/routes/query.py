from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.vector_store import search_similar

query_router = APIRouter()

@query_router.get("/")
def ask_question(q: str):
    try:
        results = search_similar(q)
        return {"question": q, "answers": results}
    except Exception as ex:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred while searching similar questions : {str(ex)}"}
        )
