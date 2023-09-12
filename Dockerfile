# Use the official Python image as the base image
FROM python:3.10.6

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV FASTAPI_ENV production

# Set the working directory inside the container
WORKDIR /api_code

# Copy the requirements.txt file and install dependencies
COPY ./requirements.txt /api_code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file into the container
COPY ./.env /api_code/.env

# Copy the entire application directory into the container
COPY ./app /api_code/app

# Expose the port your FastAPI application will run on
EXPOSE 8000

# Command to run your FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
