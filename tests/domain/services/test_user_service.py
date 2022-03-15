from unittest import TestCase
from unittest.mock import patch
from domain.models.user_model import UserModel
from domain.services.user_service import UserService
from tests.mock_data import mock_user, mock_user_invalid_document


class TestUserService(TestCase):
    @patch("domain.services.user_service.TransactionService")
    @patch("domain.services.user_service.DigitalAccountService")
    @patch("domain.services.user_service.UserRepository")
    def setUp(self, mock_user_repo, mock_digital_account_repo, mock_transaction_service) -> None:
        self.user_mock = mock_user()
        self.user_mock_invalid_document = mock_user_invalid_document()
        self.mock_user_repo = mock_user_repo
        self.mock_digital_account_repo = mock_digital_account_repo
        self.mock_transaction_service = mock_transaction_service
        self.user_service = UserService()

    def test_get_user(self):
        self.mock_user_repo().get_user.return_value = self.user_mock
        test_case = self.user_service.get_user(user_id=1)
        self.assertIsInstance(test_case, dict)

        self.mock_user_repo().get_user.return_value = None
        test_case = self.user_service.get_user(user_id=2)
        self.assertDictEqual(test_case, {})

    def test_insert_user(self):
        self.mock_user_repo().insert_user.return_value = 1
        self.mock_digital_account_repo().insert_digital_account.return_value = 10000000, 100

        result = self.user_service.insert_user(user=UserModel(**self.user_mock))
        user_id = result.get("user_id")
        digital_account_id = result.get("digital_account_id")
        digital_account_agency = result.get("digital_account_agency")

        self.assertEqual(user_id, 1)
        self.assertEqual(digital_account_agency, 100)
        self.assertEqual(digital_account_id, 10000000)

    def test_insert_user_invalid_document(self):
        result = self.user_service.insert_user(user=UserModel(**self.user_mock_invalid_document))
        user_id = result.get("user_id")
        digital_account_id = result.get("digital_account_id")
        digital_account_agency = result.get("digital_account_agency")
        self.assertIsNone(user_id)
        self.assertIsNone(digital_account_id)
        self.assertIsNone(digital_account_agency)

    def test_delete_user(self):
        self.mock_digital_account_repo().delete_digital_account.return_value = 1
        self.mock_digital_account_repo().delete_digital_account_transactions.return_value = 1
        self.mock_user_repo().delete_user.return_value = 1
        result = self.user_service.delete_user(user_id=1)
        self.assertEqual(result, True)

        self.mock_user_repo().delete_user.return_value = 0
        result = self.user_service.delete_user(user_id=1)
        self.assertEqual(result, False)
