FROM python:3.6-slim-buster

# Copy requirements.txt to the image
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python", "app.py"]