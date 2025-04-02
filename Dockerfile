# Use the official Python image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements and source files to the container
COPY requirements.txt ./
COPY devotional_bot.py ./
COPY Quotes.csv ./
COPY .env ./

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the bot
CMD ["python", "devotional_bot.py"]
