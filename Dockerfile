FROM docker.io/python:3.9-slim-bullseye

WORKDIR /app

RUN apt update && apt install -y cmake build-essential

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY people.py app.py util.py setting.py ./
COPY db ./db

CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
