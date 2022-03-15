def mock_user():
    user_mock = {
        "name": "Testonildo",
        "document": "440.784.062-54",
    }
    return user_mock


def mock_user_invalid_document():
    user_mock = {
        "name": "Testonildo",
        "document": "412.767.062-60",
    }
    return user_mock


def mock_digital_account():
    return {
        "digital_account_id": 10000000,
        "digital_account_agency": 100,
        "user_id": 1,
        "total": 4350.50,
        "withdraw_daily_limit": 2000,
        "is_active": False,
        "is_blocked": True
    }


def mock_statement():
    return [
        {
            "transaction_id": 1,
            "digital_account_id": 10000000,
            "digital_account_agency": 100,
            "transaction_type_id": 2,
            "movement_value": 5400,
            "operation_date": "2022-03-12T20:11:57"
        },
        {
            "transaction_id": 2,
            "digital_account_id": 10000000,
            "digital_account_agency": 100,
            "transaction_type_id": 1,
            "movement_value": 1000,
            "operation_date": "2022-03-12T20:11:57"
        },
        {
            "transaction_id": 3,
            "digital_account_id": 10000000,
            "digital_account_agency": 100,
            "transaction_type_id": 1,
            "movement_value": 1000,
            "operation_date": "2022-03-13T20:11:57"
        },
        {
            "transaction_id": 4,
            "digital_account_id": 10000000,
            "digital_account_agency": 100,
            "transaction_type_id": 1,
            "movement_value": 1000,
            "operation_date": "2022-03-13T20:11:57"
        },
        {
            "transaction_id": 5,
            "digital_account_id": 10000000,
            "digital_account_agency": 100,
            "transaction_type_id": 1,
            "movement_value": 1000,
            "operation_date": "2022-03-14T20:11:57"
        },
        {
            "transaction_id": 6,
            "digital_account_id": 10000000,
            "digital_account_agency": 100,
            "transaction_type_id": 1,
            "movement_value": 1000,
            "operation_date": "2022-03-14T20:11:57"
        }
    ]
