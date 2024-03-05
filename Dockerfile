# Example using the official Python 3.9 image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for Python packages with native extensions
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libffi-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy the rest of your application
COPY . .


# Command to run the bot
CMD ["python", "discord_bot.py"]
