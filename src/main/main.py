from fastapi import FastAPI

from src.exceptions.exception_handlers import init_exception_handlers
from src.price.controller import price_controller

app = FastAPI()

# Init exception handlers
init_exception_handlers(app)

# Include controllers
app.include_router(price_controller.router)