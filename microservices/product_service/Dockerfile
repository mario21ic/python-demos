FROM node:22-alpine

WORKDIR /app

COPY package.json ./
RUN npm install --only=production

COPY server.js .

EXPOSE 5002

CMD ["npm", "start"]

