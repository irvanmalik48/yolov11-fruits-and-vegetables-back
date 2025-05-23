from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")

async def get_root():
    return {"message": "Hello World"}