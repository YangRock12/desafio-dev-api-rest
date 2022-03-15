from domain.dtos.user_dto import UserDto
from domain.helpers.validate_document_helper import validate_cpf
from domain.models.user_model import UserModel
from domain.services.digital_account_service import DigitalAccountService
from domain.services.transaction_service import TransactionService
from infra.repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.digital_account_service = DigitalAccountService()
        self.transaction_service = TransactionService()

    def get_user(self, user_id: int) -> dict or None:
        user = self.user_repository.get_user(user_id=user_id)
        if user:
            return UserDto(user)
        return {}

    def insert_user(self, user: UserModel):
        user_id = None
        digital_account_id = None
        digital_account_agency_id = None

        valid_document = validate_cpf(user.document)
        if valid_document:
            user_id = self.user_repository.insert_user(user=user)
            digital_account_id = None
            if user_id:
                digital_account_id, digital_account_agency_id = \
                    self.digital_account_service.insert_digital_account(user_id=user_id)

        return {
            "user_id": user_id,
            "digital_account_id": digital_account_id,
            "digital_account_agency": digital_account_agency_id
        }

    def delete_user(self, user_id: int):
        digital_account = self.digital_account_service.get_user_digital_account(user_id=user_id)
        if digital_account:
            self.transaction_service.delete_digital_account_transactions(
                digital_account_id=digital_account.get("digital_account_id")
            )
            self.digital_account_service.delete_digital_account(
                digital_account_id=digital_account.get("digital_account_id"),
                digital_account_agency=digital_account.get("digital_account_agency")
            )
        result = self.user_repository.delete_user(user_id=user_id)
        if result > 0:
            return True
        return False

