# MCS Parakh — one image, whole demo (T-301).
# React build + FastAPI + scoring engine + synthetic dataset (DS-42-2026.07).
# Local: docker compose up → http://localhost:8000 (API docs at /api/docs).
# App Runner: same image; set PORT=8080 (or leave 8000 and configure the service port).

# ---- Stage 1: frontend build ----
FROM node:20-alpine AS webbuild
WORKDIR /web
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ---- Stage 2: runtime ----
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PARAKH_DATA=/app/data \
    PARAKH_DB=/app/parakh.db \
    PARAKH_STATIC=/app/frontend/dist

COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend/ backend/
COPY data/ data/
COPY --from=webbuild /web/dist frontend/dist

EXPOSE 8000
WORKDIR /app/backend
CMD ["sh", "-c", "uvicorn api.serve:app --host 0.0.0.0 --port ${PORT:-8000}"]
