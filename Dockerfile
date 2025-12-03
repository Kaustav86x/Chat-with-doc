FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    gcc \
    libopenblas-dev \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PIP_NO_CACHE_DIR=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# backend
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
# fronend
ENV STREAMLIT_HOST=0.0.0.0
ENV STREAMLIT_PORT=8501

# copy python dependencies file
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# copy rest
COPY app.py create_database.py query_data.py compare_embeddings.py extract_requirements.py ./
COPY frontend ./frontend

# enrypoint script and make it executable
COPY script.sh /app/script.sh
RUN chmod +x /app/script.sh

# expose ports
EXPOSE 8000 8501

ENTRYPOINT [ "/app/script.sh" ]