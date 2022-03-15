from unittest import TestCase
from unittest.mock import patch, Mock

from domain.enums.transaction_validation_enum import TransactionValidationEnum
from domain.models.transaction_model import TransactionModel
from domain.services.digital_account_service import DigitalAccountService
from tests.mock_data import mock_digital_account, mock_statement


class TestUserService(TestCase):
    @patch("domain.services.transaction_service.TransactionRepository")
    @patch("domain.services.digital_account_service.DigitalAccountRepository")
    def setUp(self, mock_digital_account_repo, mock_transaction_repo) -> None:
        self.mock_digital_account_repo = mock_digital_account_repo
        self.mock_transaction_repo = mock_transaction_repo

        self.digital_account_mock = mock_digital_account()
        self.mock_statement = mock_statement()

        self.digital_account_service = DigitalAccountService()

    def test_get_user_digital_account(self):
        self.mock_digital_account_repo().get_user_digital_account.return_value = self.digital_account_mock
        result = self.digital_account_service.get_user_digital_account(user_id=1)
        self.assertEqual(result.get("digital_account_id"), 10000000)
        self.assertEqual(result.get("digital_account_agency"), 100)
        self.assertEqual(result.get("total"), 4350.50)
        self.assertEqual(result.get("is_active"), False)
        self.assertEqual(result.get("is_blocked"), True)

        self.mock_digital_account_repo().get_user_digital_account.return_value = None
        result = self.digital_account_service.get_user_digital_account(user_id=2)
        self.assertEqual(result, {})

    def test_change_status(self):
        self.mock_digital_account_repo().change_account_active_status.return_value = not self.digital_account_mock.get(
            "is_active")

        result = self.digital_account_service.change_account_active_status(digital_account_id=10000000,
                                                                           digital_account_agency=100)
        self.assertTrue(result)

        self.digital_account_mock["is_active"] = True
        self.mock_digital_account_repo().change_account_active_status.return_value = not self.digital_account_mock.get(
            "is_active")

        result = self.digital_account_service.change_account_active_status(digital_account_id=10000000,
                                                                           digital_account_agency=100)
        self.assertFalse(result)
        self.digital_account_mock["is_active"] = False

        self.mock_digital_account_repo().change_account_block_status.return_value = not self.digital_account_mock.get(
            "is_blocked")

        result = self.digital_account_service.change_account_block_status(digital_account_id=10000000,
                                                                          digital_account_agency=100)
        self.assertFalse(result)

        self.digital_account_mock["is_blocked"] = False
        self.mock_digital_account_repo().change_account_block_status.return_value = not self.digital_account_mock.get(
            "is_blocked")

        result = self.digital_account_service.change_account_block_status(digital_account_id=10000000,
                                                                          digital_account_agency=100)
        self.assertTrue(result)
        self.digital_account_mock["is_blocked"] = True

    def test_statement_by_period_passing_dates(self):
        self.mock_transaction_repo().get_statement_by_period.return_value = self.mock_statement

        result = self.digital_account_service.get_statement_by_period(digital_account_id=10000000,
                                                                      digital_account_agency=100,
                                                                      start_date="20220312",
                                                                      end_date="20220315")
        min_operation_date = min([date.get("operation_date") for date in result])
        max_operation_date = max([date.get("operation_date") for date in result])
        self.assertEqual(len(result), 6)
        self.assertGreaterEqual(min_operation_date, "2022-03-12T00:00:00")
        self.assertEqual(min_operation_date, "2022-03-12T20:11:57")
        self.assertLessEqual(max_operation_date, "2022-03-15T23:59:59")
        self.assertEqual(max_operation_date, "2022-03-14T20:11:57")

    def test_statement_by_period_without_passing_dates(self):
        self.mock_transaction_repo().get_statement_by_period.return_value = self.mock_statement

        result = self.digital_account_service.get_statement_by_period(digital_account_id=10000000,
                                                                      digital_account_agency=100)
        min_operation_date = min([date.get("operation_date") for date in result])
        max_operation_date = max([date.get("operation_date") for date in result])
        self.assertEqual(len(result), 6)
        self.assertGreaterEqual(min_operation_date, "2022-03-01T00:00:00")
        self.assertEqual(min_operation_date, "2022-03-12T20:11:57")
        self.assertLessEqual(max_operation_date, "2022-03-31T23:59:59")
        self.assertEqual(max_operation_date, "2022-03-14T20:11:57")

    @patch("domain.strategies.deposit_strategy.DigitalAccountRepository")
    @patch("domain.services.transaction_service.TransactionRepository")
    def test_do_transaction_account_inactive(self, mock_transaction_repo, mock_digital_account_repo):
        mock_digital_account_repo.return_value = Mock()
        mock_transaction_repo.return_value = Mock()
        self.mock_digital_account_repo().get_digital_account.return_value = self.digital_account_mock

        transaction_model = TransactionModel(digital_account_id=10000000,
                                             digital_account_agency=100,
                                             transaction_type_id=2,
                                             value=5400.85)
        test_case = self.digital_account_service.do_transaction(transaction_model=transaction_model)
        self.assertIsInstance(test_case, dict)

        result = test_case.get("result")
        transaction = test_case.get("transaction")
        self.assertEqual(result, False)
        self.assertEqual(transaction, 'deposit')

    @patch("domain.strategies.deposit_strategy.DigitalAccountRepository")
    @patch("domain.services.transaction_service.TransactionRepository")
    def test_do_transaction_account_blocked(self, mock_transaction_repo, mock_digital_account_repo):
        mock_digital_account_repo.return_value = Mock()
        mock_transaction_repo.return_value = Mock()

        self.mock_digital_account_repo().change_account_active_status.return_value = not self.digital_account_mock.get(
            "is_active")
        self.digital_account_mock["is_active"] = self.digital_account_service.change_account_active_status(
            digital_account_id=10000000,
            digital_account_agency=100)

        self.mock_digital_account_repo().get_digital_account.return_value = self.digital_account_mock

        transaction_model = TransactionModel(digital_account_id=10000000,
                                             digital_account_agency=100,
                                             transaction_type_id=2,
                                             value=5400.85)
        test_case = self.digital_account_service.do_transaction(transaction_model=transaction_model)
        self.assertIsInstance(test_case, dict)

        result = test_case.get("result")
        transaction = test_case.get("transaction")
        self.assertEqual(result, False)
        self.assertEqual(transaction, 'deposit')

        self.digital_account_mock["is_active"] = False

    @patch("domain.strategies.deposit_strategy.DigitalAccountRepository")
    @patch("domain.services.transaction_service.TransactionRepository")
    def test_do_transaction_deposit_ok(self, mock_transaction_repo, mock_digital_account_repo):
        mock_digital_account_repo().do_deposit.return_value = True
        mock_transaction_repo.return_value = Mock()

        self.mock_digital_account_repo().change_account_active_status.return_value = not self.digital_account_mock.get(
            "is_active")
        self.mock_digital_account_repo().change_account_block_status.return_value = not self.digital_account_mock.get(
            "is_blocked")
        self.digital_account_mock["is_active"] = self.digital_account_service.change_account_active_status(
            digital_account_id=10000000,
            digital_account_agency=100)
        self.digital_account_mock["is_blocked"] = self.digital_account_service.change_account_block_status(
            digital_account_id=10000000,
            digital_account_agency=100)

        self.mock_digital_account_repo().get_digital_account.return_value = self.digital_account_mock

        transaction_model = TransactionModel(digital_account_id=10000000,
                                             digital_account_agency=100,
                                             transaction_type_id=2,
                                             value=5400.85)
        test_case = self.digital_account_service.do_transaction(transaction_model=transaction_model)
        self.assertIsInstance(test_case, dict)

        result = test_case.get("result")
        transaction = test_case.get("transaction")
        self.assertEqual(result, True)
        self.assertEqual(transaction, 'deposit')

        self.digital_account_mock["is_active"] = False
        self.digital_account_mock["is_blocked"] = True

    @patch("domain.strategies.withdraw_strategy.DigitalAccountRepository")
    @patch("domain.services.transaction_service.TransactionRepository")
    def test_do_transaction_withdraw_no_balance_available(self, mock_transaction_repo, mock_digital_account_repo):
        mock_digital_account_repo().do_withdraw.return_value = True
        mock_transaction_repo.return_value = Mock()

        self.mock_digital_account_repo().change_account_active_status.return_value = not self.digital_account_mock.get(
            "is_active")
        self.mock_digital_account_repo().change_account_block_status.return_value = not self.digital_account_mock.get(
            "is_blocked")
        self.digital_account_mock["is_active"] = self.digital_account_service.change_account_active_status(
            digital_account_id=10000000,
            digital_account_agency=100)
        self.digital_account_mock["is_blocked"] = self.digital_account_service.change_account_block_status(
            digital_account_id=10000000,
            digital_account_agency=100)

        self.mock_digital_account_repo().get_digital_account.return_value = self.digital_account_mock

        transaction_model = TransactionModel(digital_account_id=10000000,
                                             digital_account_agency=100,
                                             transaction_type_id=1,
                                             value=5400.85)
        test_case = self.digital_account_service.do_transaction(transaction_model=transaction_model)
        self.assertIsInstance(test_case, dict)

        result = test_case.get("result")
        transaction = test_case.get("transaction")
        self.assertEqual(result, False)
        self.assertEqual(transaction, 'withdraw')

        self.digital_account_mock["is_active"] = False
        self.digital_account_mock["is_blocked"] = True

    @patch("domain.strategies.withdraw_strategy.DigitalAccountRepository")
    @patch("domain.services.transaction_service.TransactionRepository")
    def test_do_transaction_withdraw_no_limit_available(self, mock_transaction_repo, mock_digital_account_repo):
        mock_digital_account_repo().do_withdraw.return_value = True
        mock_transaction_repo.return_value = Mock()

        self.mock_digital_account_repo().change_account_active_status.return_value = not self.digital_account_mock.get(
            "is_active")
        self.mock_digital_account_repo().change_account_block_status.return_value = not self.digital_account_mock.get(
            "is_blocked")
        self.digital_account_mock["is_active"] = self.digital_account_service.change_account_active_status(
            digital_account_id=10000000,
            digital_account_agency=100)
        self.digital_account_mock["is_blocked"] = self.digital_account_service.change_account_block_status(
            digital_account_id=10000000,
            digital_account_agency=100)

        self.mock_digital_account_repo().get_digital_account.return_value = self.digital_account_mock

        transaction_model = TransactionModel(digital_account_id=10000000,
                                             digital_account_agency=100,
                                             transaction_type_id=1,
                                             value=3000)
        test_case = self.digital_account_service.do_transaction(transaction_model=transaction_model)
        self.assertIsInstance(test_case, dict)

        result = test_case.get("result")
        transaction = test_case.get("transaction")
        self.assertEqual(result, False)
        self.assertEqual(transaction, 'withdraw')

        self.digital_account_mock["is_active"] = False
        self.digital_account_mock["is_blocked"] = True

    @patch("domain.strategies.withdraw_strategy.DigitalAccountRepository")
    @patch("domain.services.transaction_service.TransactionRepository")
    def test_do_transaction_withdraw_ok(self, mock_transaction_repo, mock_digital_account_repo):
        mock_digital_account_repo().do_withdraw.return_value = True
        mock_transaction_repo.return_value = Mock()

        self.mock_digital_account_repo().change_account_active_status.return_value = not self.digital_account_mock.get(
            "is_active")
        self.mock_digital_account_repo().change_account_block_status.return_value = not self.digital_account_mock.get(
            "is_blocked")
        self.digital_account_mock["is_active"] = self.digital_account_service.change_account_active_status(
            digital_account_id=10000000,
            digital_account_agency=100)
        self.digital_account_mock["is_blocked"] = self.digital_account_service.change_account_block_status(
            digital_account_id=10000000,
            digital_account_agency=100)

        self.mock_digital_account_repo().get_digital_account.return_value = self.digital_account_mock

        transaction_model = TransactionModel(digital_account_id=10000000,
                                             digital_account_agency=100,
                                             transaction_type_id=1,
                                             value=2000)
        test_case = self.digital_account_service.do_transaction(transaction_model=transaction_model)
        self.assertIsInstance(test_case, dict)

        result = test_case.get("result")
        transaction = test_case.get("transaction")
        self.assertEqual(result, True)
        self.assertEqual(transaction, 'withdraw')

        self.digital_account_mock["is_active"] = False
        self.digital_account_mock["is_blocked"] = True
