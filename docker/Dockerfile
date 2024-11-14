FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /fastapi_biwoco

COPY requirements.txt /fastapi_biwoco/requirements.txt
RUN pip install --no-cache-dir -r /fastapi_biwoco/requirements.txt

COPY app/ /fastapi_biwoco/app
COPY celery_task/ /fastapi_biwoco/celery_task
COPY core/ /fastapi_biwoco/core
COPY main.py /fastapi_biwoco/main.py
COPY .env /fastapi_biwoco/.env

EXPOSE 8000

CMD ["python", "main.py", "--env", "local"]
