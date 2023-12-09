FROM python:3.9

WORKDIR /app

RUN pip3 install --upgrade Flask requests dataclasses

COPY . /app

ENTRYPOINT ["python", "ocr-server.py"]