from domain.models.user_model import UserModel


class UserDto:
    def __new__(cls, user: dict) -> dict:
        result = UserModel(**user)
        return result.dict()
