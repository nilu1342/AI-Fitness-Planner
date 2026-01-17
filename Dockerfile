# Use Python 3.11.9 base image
FROM python:3.11.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose port 8080 (Render default)
EXPOSE 8080

# Command to run your app
# If using Streamlit:
# CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
# If using Flask:
CMD ["python", "app.py"]
