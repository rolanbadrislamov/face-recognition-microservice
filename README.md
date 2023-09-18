# Face Recognition Microservice

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.101%2B-green)
![Deepface](https://img.shields.io/badge/Deepface-0.0.79%2B-yellow)
![MongoDB](https://img.shields.io/badge/MongoDB-6.0%2B-brightgreen)
![Docker](https://img.shields.io/badge/Docker-24.0%2B-blue)

This asynchronous facial recognition microservice is designed for easy integration into applications with a microservices architecture using Docker containerization.

## Overview

- Efficient facial recognition using asynchronous programming and Deepface caching enables rapid identification of **100+** profiles in under **10 seconds** per image.
- Robust JWT authentication and authorization mechanisms enhance the security of sensitive data and protect API endpoints.

## Deployment

### FastAPI Application Only

To deploy the FastAPI application without MongoDB, run the following command:

```shell
uvicorn app.main:app --reload
```
### Deploy with MongoDB using Docker Compose
1. Make sure you have Docker and Docker Compose installed on your system

2. Clone this repository to your local machine:
```shell
git clone https://github.com/rolanbadrislamov/face-recognition-microservice.git
```
3.Create a .env file in the project root directory and configure your environment variables.

4.Build and run the Docker containers using Docker Compose:
```shell
docker-compose up --build
```

This will start the FastAPI application and a MongoDB container. You can access the microservice at http://localhost:8000.

Make sure to customize the configuration and environment variables as needed for your specific deployment.

## Documentation
For detailed API documentation and usage examples, please refer to the API documentation provided with the microservice. You can typically access the documentation at http://localhost:8000/docs when running the microservice locally.

Feel free to reach out if you have any questions or need further assistance with deploying and using this facial recognition microservice.
