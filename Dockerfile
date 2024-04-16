FROM python:3-slim

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY . /app

COPY requirements.txt .

RUN python -m pip install -U pip
RUN python -m pip install -r requirements.txt

ENTRYPOINT [ "python", "src/app.py" ]