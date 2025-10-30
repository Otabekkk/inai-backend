FROM python:3.13

WORKDIR /code

COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
