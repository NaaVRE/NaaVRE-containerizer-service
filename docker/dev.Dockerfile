FROM python:3.12

ENV ROOT_PATH /

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD fastapi dev app/main.py --port 8000 --root-path "$ROOT_PATH" --host 0.0.0.0
