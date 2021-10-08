FROM python:3.8.5

WORKDIR /code

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
CMD python manage.py makemigrations --noinput
CMD python manage.py migrate --noinput
CMD python manage.py collectstatic --noinput
