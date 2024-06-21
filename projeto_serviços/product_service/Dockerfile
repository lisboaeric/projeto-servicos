FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY product_db.sqlite /app/product_db.sqlite
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8002"]
