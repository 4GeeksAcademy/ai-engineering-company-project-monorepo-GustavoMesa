FROM python:3.11-slim

WORKDIR /app

COPY services/requirements.txt ./services/requirements.txt
RUN pip install --no-cache-dir -r services/requirements.txt

COPY services/main.py ./services/main.py
COPY src/ ./src/

RUN mkdir -p /app/data

EXPOSE 8000

CMD ["uvicorn", "services.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
