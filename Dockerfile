# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Clone the repository
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/KenKout/OCR-AI.git /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Add index.html to Streamlit folder
RUN mv static/index.html /usr/local/lib/python3.9/site-packages/streamlit/static/index.html

# Run app.py when the container launches
CMD ["python", "run.py"]
