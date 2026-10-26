# ============================================
# BRASALAND — BACKOFFICE (Next.js)
# Multi-stage build: builder + runner
# ============================================

# ---- BUILDER ----
FROM node:18-alpine AS builder

WORKDIR /app

# Dependencias primero (capa cacheable)
COPY package.json package-lock.json* ./
RUN npm install

# Código fuente y compilación
COPY . .
RUN npm run build

# ---- RUNNER (producción) ----
FROM node:18-alpine AS runner

WORKDIR /app

# Solo lo necesario para servir la app compilada
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Puerto de escucha
EXPOSE 3001

# Arrancar en modo producción
ENV NODE_ENV=production
CMD ["npm", "start"]