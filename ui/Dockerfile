# Use the official Python image as base
FROM python:3.9-slim

# Install libs
RUN pip install streamlit requests

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 5000
EXPOSE 80

CMD ["streamlit", "run", "app.py", "--server.port", "80"]