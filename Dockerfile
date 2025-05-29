FROM python:3.11-slim

WORKDIR /app

COPY exporter.py config.yaml ./

RUN pip install --no-cache-dir flask prometheus_client requests pyyaml

EXPOSE 9345

CMD ["python", "exporter.py"]
