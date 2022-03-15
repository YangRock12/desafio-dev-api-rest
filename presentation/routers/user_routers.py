from fastapi import APIRouter
from fastapi.responses import JSONResponse

from domain.models.user_model import UserModel
from domain.services.user_service import UserService

router = APIRouter(
    prefix="/user"
)

user_service = UserService()


@router.get("/{user_id}")
def get_user(user_id: int):
    result = user_service.get_user(user_id=user_id)
    return JSONResponse(status_code=200, content={"user": result})


@router.post("/")
def insert_user(user: UserModel):
    result = user_service.insert_user(user=user)
    user_id = result.get("user_id")
    if user_id:
        return JSONResponse(status_code=201, content={"message": result})
    return JSONResponse(status_code=500, content={"message": "Something went wrong"})


@router.delete("/{user_id}")
def delete_user(user_id: int):
    result = user_service.delete_user(user_id=user_id)
    if result:
        return JSONResponse(status_code=200, content={"message": "user deleted"})
    return JSONResponse(status_code=500, content={"message": "Something went wrong"})