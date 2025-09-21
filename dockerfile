FROM python:3.11 as build

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./src /code/src

COPY ./scripts/setup.py /code/setup.py

COPY ./.env /code/.env

RUN python setup.py

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8002"]