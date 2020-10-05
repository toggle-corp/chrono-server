FROM python:3.8.2-buster

LABEL maintainer="Togglecorp Dev dev@togglecorp.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]

