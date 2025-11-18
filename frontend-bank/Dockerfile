# Build stage
FROM node:20-alpine as build

WORKDIR /app

ARG VITE_backend_url
ENV VITE_backend_url=$VITE_backend_url

COPY package.json .

RUN npm install

RUN npm i -g serve

COPY . .

RUN npm run build

EXPOSE 3000

CMD [ "serve", "-s", "dist" ]
