# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /founds

# Copy the rest of the application code into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]