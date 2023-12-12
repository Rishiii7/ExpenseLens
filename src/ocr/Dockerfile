FROM python:3.9

WORKDIR /app

RUN pip3 install --upgrade Flask requests dataclasses redis

COPY . /app

ENTRYPOINT ["python3", "ocr-server.py"]