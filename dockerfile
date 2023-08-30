FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev
    
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5050

CMD ["python", "app.py"]
