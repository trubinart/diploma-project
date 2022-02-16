#из какого образа создаем контейнер
FROM python:3.8-slim-buster

#название рабочей директории внутри контейнера
WORKDIR /app

#команды для выполнения внутри докера
RUN apt-get update
RUN apt-get install -y build-essential python-dev

RUN pip3 install --upgrade pip
RUN pip3 install uwsgi

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV PRODUCTION
ENV DJANGO_SETTINGS_MODULE habr.settings

#копирование из папки где лежит докуерфайл в папку /app
COPY . .

#обновление времени в контейнере
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#команда которая выполниться в консоли
#CMD [ "uwsgi", "--http", ":9090", "--wsgi-file", "modules/main.py"]
#CMD [ "python3", "run.py"]
CMD [ "python3", "manage.py", "collectstatic"]
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:9090"]