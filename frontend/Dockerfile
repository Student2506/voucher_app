FROM node:20-alpine3.16
RUN apk update && apk add --update --no-cache \
	g++ \
	make \
	py3-pip
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN npm ci --omit=dev
COPY . .
EXPOSE 3000
