FROM python:3.11-slim

WORKDIR /app

# For psycopg2 building
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copy dependencies and download them
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt --verbose

# Copy all project
Copy . .

# Open (expose) 8000 port
EXPOSE 8000

#CMD Pytest

CMD ["python", "main.py"]