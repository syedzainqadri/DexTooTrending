# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install wget, curl, unzip, and necessary libraries for Google Chrome
RUN apt-get update && \
    apt-get install -y wget gnupg2 curl unzip \
                       fonts-liberation libappindicator3-1 libasound2 \
                       libatk-bridge2.0-0 libatk1.0-0 libcups2 \
                       libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 \
                       libx11-xcb1 xdg-utils

# Download and install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# Install Firefox
RUN apt-get update && apt-get install -y wget firefox-esr \
    && wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.29.0-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/ \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* geckodriver-v0.29.0-linux64.tar.gz

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "multipro.py"]
