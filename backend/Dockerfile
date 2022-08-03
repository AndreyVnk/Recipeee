FROM python:3.7-slim
# RUN apt update && apt -y install libpq-dev build-essential
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
