FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Create directory for the persistent volume mount
RUN mkdir -p /dhruv_PV_dir
# Expose the port
EXPOSE 6000

CMD ["python", "app.py"]