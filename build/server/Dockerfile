FROM python:3-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY . /app

COPY requirements.txt .

RUN python -m pip install -U pip
RUN python -m pip install -r requirements.txt

FROM base as debugpy
RUN python -m pip install debugpy
ENV FLASK_DEBUG=false
CMD ["python", "-m", "debugpy", "--wait-for-client", "--listen", "0.0.0.0:5678", "src/app.py"]W

FROM base as main
ENV FLASK_DEBUG=true
ENTRYPOINT [ "flask", "--app=src.backend:create_app", "run", "--host=0.0.0.0"]