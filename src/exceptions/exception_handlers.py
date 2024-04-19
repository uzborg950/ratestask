# from src.main.main import app

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse




class RequestValidationException(Exception):
    def __init__(self, param_name: str, param_value: str, extra_message=''):
        self.param_name = param_name
        self.param_value = param_value
        self.extra_message = extra_message


class InvalidDateRangeException(Exception):
    def __init__(self, date_from_param: str, date_from_value: str, date_to_param: str, date_to_value: str):
        self.date_from_param = date_from_param
        self.date_from_value = date_from_value
        self.date_to_param = date_to_param
        self.date_to_value = date_to_value


def init_exception_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationException)
    async def request_validation_exception_hander(request: Request, exc: RequestValidationException):
        return JSONResponse(
            status_code=422,
            content={
                "message": f"invalid parameter sent in request: {exc.param_name}->{exc.param_value}.{' ' + exc.extra_message if exc.extra_message else ''}"},
        )

    @app.exception_handler(InvalidDateRangeException)
    async def invalid_date_range_exception_hander(request: Request, exc: InvalidDateRangeException):
        return JSONResponse(
            status_code=422,
            content={
                "message": f"invalid date range entered in parameter: {exc.date_from_param}: {exc.date_from_value} -> {exc.date_to_param}: {exc.date_to_value}."},
        )
