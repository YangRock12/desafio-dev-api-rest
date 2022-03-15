import uvicorn
from fastapi import FastAPI

from api_description import get_description
from cross_cutting.configs import SERVER_PORT, SERVER_HOST
from presentation.routers.digital_account_routers import router as digital_account_router
from presentation.routers.user_routers import router as user_router

description = get_description()

app = FastAPI(title="DigitalAccountAPI",
              description=description)

app.include_router(
    router=user_router,
    tags=["user"]
)
app.include_router(
    router=digital_account_router,
    tags=["digital_account"]
)


if __name__ == "__main__":
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
