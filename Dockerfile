FROM python:3.11.6

WORKDIR /app

COPY . .

CMD ["python", "Terminal_bot/main.py"]

