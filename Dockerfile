FROM python:3.6

RUN mkdir /var/www
WORKDIR /var/www

RUN pip install pipenv

COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock
ENV PIPENV_VENV_IN_PROJECT true
RUN pipenv install
ENV PYTHONPATH $PYTHONPATH:/var/www

COPY ./app ./app

CMD ["pipenv", "run", "uwsgi", "--ini", "/var/www/app/config/uwsgi.ini"]
