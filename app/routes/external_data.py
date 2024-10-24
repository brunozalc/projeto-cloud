from fastapi import APIRouter, Depends, HTTPException

from app.services import external_data
from app.utils.jwt import get_current_user

router = APIRouter()


@router.get("/consultar")
async def get_external_data(current_user: dict = Depends(get_current_user)):
    return await external_data.get_external_data(current_user)
