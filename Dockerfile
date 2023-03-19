# Use the official Python base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requierements.txt .

# Install the dependencies
RUN pip install --trusted-host pypi.python.org -r requierements.txt

COPY pfizer_test.py constants.py ./

# Copy the pfizer_test.py file into the container
COPY pfizer_test.py .

# Run the Python script when the container starts
CMD ["python", "pfizer_test.py"]

