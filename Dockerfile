FROM python:3.11-slim

WORKDIR /python-app

COPY . .

CMD ["python", "main.py"]





