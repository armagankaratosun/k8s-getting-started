# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the app code into the container
COPY app.py /app

# Install Flask
RUN pip install Flask

# Expose the port the app runs on
EXPOSE 8080

# Define the command to run the app
CMD ["python", "app.py"]
