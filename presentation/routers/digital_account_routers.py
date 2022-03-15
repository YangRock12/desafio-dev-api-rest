from fastapi import APIRouter
from fastapi.responses import JSONResponse

from domain.models.digital_account_model import DigitalAccountModel
from domain.models.message_response_model import MessageResponseModel
from domain.models.transaction_model import TransactionModel
from domain.services.digital_account_service import DigitalAccountService

router = APIRouter(
    prefix="/digital_account"
)

digital_account_service = DigitalAccountService()


@router.get("/{user_id}",
            response_model=DigitalAccountModel)
def get_user_digital_account(user_id: int):
    result = digital_account_service.get_user_digital_account(user_id=user_id)
    return JSONResponse(status_code=200, content={"digital_account": result})


@router.get("/statement/")
def get_statement_by_period(digital_account_id: int,
                            digital_account_agency: int,
                            start_date: str = None,
                            end_date: str = None):
    result = digital_account_service.get_statement_by_period(start_date=start_date,
                                                             end_date=end_date,
                                                             digital_account_id=digital_account_id,
                                                             digital_account_agency=digital_account_agency)
    return {"statement": result}


@router.post("/transaction",
             responses={
                 201: {"model": MessageResponseModel, "description": "Transaction Made Successfully"},
                 403: {"model": MessageResponseModel, "description": "Validation Error"},
                 500: {"model": MessageResponseModel, "description": "Something went wrong"},
                 501: {"model": MessageResponseModel, "description": "Not Implemented"},
             })
def do_digital_account_transaction(transaction_model: TransactionModel = None):
    response = digital_account_service.do_transaction(transaction_model=transaction_model)
    result = response.get("result", None)
    transaction = response.get("transaction", None)
    if result:
        return JSONResponse(status_code=201, content={"message": "Transaction Made Successfully"})
    else:
        if transaction != "unknown":
            return JSONResponse(status_code=403, content={"message": f"{transaction} could not be made"})
        elif transaction == "unknown":
            return JSONResponse(status_code=501, content={"message": "Transaction could not be identified"})
    return JSONResponse(status_code=500, content={"message": "Something went wrong"})


@router.put("/change_active_status")
def change_account_active_status(digital_account_id: int, digital_account_agency: int):
    result = digital_account_service.change_account_active_status(digital_account_id=digital_account_id,
                                                                  digital_account_agency=digital_account_agency)
    if result:
        return JSONResponse(status_code=200, content={"message": "ok"})
    return JSONResponse(status_code=500, content={"message": "Something went wrong"})


@router.put("/change_blocked_status")
def change_account_block_status(digital_account_id: int, digital_account_agency: int):
    result = digital_account_service.change_account_block_status(digital_account_id=digital_account_id,
                                                                 digital_account_agency=digital_account_agency)
    if result:
        return JSONResponse(status_code=200, content={"message": "ok"})
    return JSONResponse(status_code=500, content={"message": "Something went wrong"})
