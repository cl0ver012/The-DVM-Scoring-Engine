FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY dvm_scoring /app/dvm_scoring
COPY data /app/data

CMD ["python", "-m", "dvm_scoring.main", "data/mock_data.json"]

