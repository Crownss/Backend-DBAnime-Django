FROM python:3.9-slim

WORKDIR /DBAnime

COPY . /DBAnime/

#let this alone
ENV PYTHONUNBUFFERED=1

#Email config
ENV EMAIL_BACKEND=${EMAIL_BACKEND}
ENV EMAIL_HOST=${EMAIL_HOST}
ENV EMAIL_PORT=${EMAIL_PORT}
ENV EMAIL_USE_TLS=${EMAIL_USE_TLS}
ENV EMAIL_HOST_USER=${EMAIL_HOST_USER}
ENV EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}

#Settings config
ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=${DEBUG}
ENV SECURE_SSL_REDIRECT=${SECURE_SSL_REDIRECT}
ENV ALLOWED_HOSTS=${ALLOWED_HOSTS}
ENV CORS_ORIGIN_WHITELIST=${CORS_ORIGIN_WHITELIST}

#Database config
ENV database_engine=${database_engine}
ENV database_name=${database_name}
ENV database_user=${database_user}
ENV database_password=${database_password}
ENV database_host=${database_host}
ENV database_port=${database_port}

RUN pip install -r requirements.txt

RUN python manage.py makemigrations

RUN python manage.py migrate

RUN python manage.py collectstatic

RUN sh create_superuser.sh

ENTRYPOINT [ "gunicorn", "--preload", "-t", "3", "--worker-class=gevent", "--worker-connections=1000", "-w", "5", "--threads", "5", "Settings.wsgi" ]