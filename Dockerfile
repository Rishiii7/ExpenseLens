FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "app.py"]