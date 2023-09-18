# Use a lightweight base image
FROM python:3.10.6-slim AS base

ENV PYTHONUNBUFFERED 1
ENV FASTAPI_ENV production

RUN apt-get update && apt-get install -y python3-opencv && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /api_code

COPY ./requirements.txt /api_code/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /api_code

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
