FROM python:3.8

RUN apt update -y && apt install awscli -y
WORKDIR /deploy_app

COPY . /deploy_app
RUN pip install -r requirements.txt

CMD ["python3", "/app/main.py"]