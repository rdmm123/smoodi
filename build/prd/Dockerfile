FROM node:18-alpine as build-fe

WORKDIR /app
COPY ./*.json /app
COPY ./*.ts /app
COPY ./*.js /app

COPY ./src/frontend /app/src/frontend
COPY ./build.prd/.env_fe /app/.env

COPY package.json .

RUN npm install
RUN npm run build

FROM python:3-slim as server

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

COPY requirements.txt .

RUN python -m pip install -U pip
RUN python -m pip install -r requirements.txt
RUN python -m pip install gunicorn

COPY --from=build-fe /app/src/frontend/dist /app/src/frontend/dist

ENV FLASK_ENV=production
CMD exec gunicorn --bind :2107 --workers=1 --threads=8 --timeout=0 --access-logfile=- 'src.backend:create_app()'