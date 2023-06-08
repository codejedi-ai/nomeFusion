# Use a Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the main.py file to the container
COPY main.py .

# Copy the requirements.txt file to the container
COPY requirements.txt .
COPY script.sh .
COPY .env .
# Install dependencies
RUN python -m venv venv
RUN . venv/bin/activate && pip install -r requirements.txt


# Run the main.py script
CMD ["/bin/bash", "script.sh"]