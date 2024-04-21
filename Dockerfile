FROM python:3.9
WORKDIR /rates-api
COPY ./requirements.txt /rates-api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /rates-api/requirements.txt
COPY ./src /rates-api/src
CMD ["uvicorn", "src.main.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
    