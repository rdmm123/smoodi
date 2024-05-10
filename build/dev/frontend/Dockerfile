FROM node:18-alpine

WORKDIR /app
COPY ./*.json /app
COPY ./*.ts /app
COPY ./*.js /app

COPY ./src/frontend /app/src/frontend
COPY ./build/dev/frontend/.env /app

COPY package.json .

RUN npm install

EXPOSE 5001

CMD [ "npm", "run", "dev" ]