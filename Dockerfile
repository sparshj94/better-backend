FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy project
COPY . .

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"] 