FROM python:3.12-slim

# ---- system deps ----
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# ---- python deps ----
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- project ---- 
COPY . /app
ENV PYTHONUNBUFFERED=1
EXPOSE 8501

CMD ["streamlit", "run", "app/app.py", "--server.port", "8501", "--server.headless=true"]
