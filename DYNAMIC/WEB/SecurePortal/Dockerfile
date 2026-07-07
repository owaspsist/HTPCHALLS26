FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENV FLAG=warCTF{test_flag_placeholder}

EXPOSE 5000

CMD ["python", "app.py"]
