# ---- Base image ----
FROM python:3.10-slim

# ---- Environment ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Workdir ----
WORKDIR /app

# ---- Install system# ---------- Base ----------
FROM python:3.10-slim

# ---------- System deps ----------
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---------- Working directory ----------
WORKDIR /app

# ---------- Install dependencies ----------
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Copy backend code ----------
COPY backend/app ./app

# ---------- Expose Railway port ----------
EXPOSE 8000

# ---------- Start server ----------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
deps ----
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Copy backend only ----
COPY backend/ backend/

# ---- Install Python deps ----
RUN python -m pip install --upgrade pip \
    && python -m pip install -r backend/requirements.txt

# ---- Expose port ----
EXPOSE 8000

# ---- Start server ----
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
