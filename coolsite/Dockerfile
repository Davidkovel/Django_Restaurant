#FROM python:3.9
#
#WORKDIR /app
#
#COPY ./requirements.txt ./
#RUN pip install -r requirements.txt
#COPY . .

FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app

RUN mkdir /app/static && mkdir /app/media

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver"]
