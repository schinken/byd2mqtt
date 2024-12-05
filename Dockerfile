FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir paho-mqtt
COPY byd.py /app/byd.py

CMD ["python", "byd.py"]