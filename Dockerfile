FROM python:3.8.5
RUN mkdir /fixtures
COPY fixtures /fixtures
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY foodgram-project .
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000