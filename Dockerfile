FROM python:3-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY . /app

COPY requirements.txt .

RUN python -m pip install -U pip
RUN python -m pip install -r requirements.txt

FROM base as debugpy
RUN pip install debugpy
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5679", "app.py"]


FROM base as main
ENTRYPOINT [ "python", "src/app.py" ]