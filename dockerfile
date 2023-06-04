# Use a Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the main.py file to the container
COPY main.py .

# Copy the .env file to the container
COPY .env .

# Install dependencies
RUN python -m venv venv
RUN . venv/bin/activate && pip install -r requirements.txt

# Set the Discord token as a build argument
ARG DISCORD_TOKEN

# Set the environment variable using the build argument
ENV DISCORD_TOKEN=${DISCORD_TOKEN}

# Run the main.py script
CMD [ "python", "main.py" ]
