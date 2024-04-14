# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Firefox and the necessary utilities
RUN apt-get update \
    && apt-get install -y --no-install-recommends firefox-esr wget \
    && wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz \
    && tar -xzf geckodriver-v0.29.0-linux64.tar.gz -C /usr/local/bin \
    && apt-get purge -y --auto-remove wget \
    && rm -rf /var/lib/apt/lists/* \
    && rm geckodriver-v0.29.0-linux64.tar.gz

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 4444 available to the world outside this container
EXPOSE 4444

# Define environment variable
ENV HEADLESS true

# Run the Python script when the container launches
CMD ["python", "your_script.py"]
