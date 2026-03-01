from fastapi import APIRouter

router = APIRouter()

@router.get("/flights")
def get_flights():
    return {"message": "list of flights"}
