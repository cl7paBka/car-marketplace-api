FROM python:3.11-slim

WORKDIR /app

# Copy dependencies and download them
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy all project
Copy . .

# Open (expose) 8000 port
EXPOSE 8000

CMD ["python", "main.py"]