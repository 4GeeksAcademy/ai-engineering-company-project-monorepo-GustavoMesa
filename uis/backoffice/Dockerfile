FROM node:20-alpine AS dependencies

WORKDIR /app

COPY package*.json ./
RUN npm ci

FROM dependencies AS development

COPY . .

EXPOSE 3001

CMD ["npm", "run", "dev", "--", "-p", "3001", "-H", "0.0.0.0"]

FROM dependencies AS builder

ARG INVENTORY_API_URL=http://services:8000/api/v1/inventory
ENV INVENTORY_API_URL=${INVENTORY_API_URL}

COPY . .
RUN mkdir -p public && npm run build

FROM node:20-alpine AS production

WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3001
ENV HOSTNAME=0.0.0.0

COPY --from=builder --chown=node:node /app/.next/standalone ./
COPY --from=builder --chown=node:node /app/.next/static ./.next/static
COPY --from=builder --chown=node:node /app/public ./public

USER node
EXPOSE 3001
CMD ["node", "server.js"]
