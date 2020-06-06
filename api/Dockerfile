FROM python:3.6

LABEL maintainer="vinh-ngu@hotmail.com"

WORKDIR /app
ADD . .
RUN pip install -r requirements.txt

EXPOSE 5000
CMD gunicorn -w 5 --bind 0.0.0.0:5000 wsgi:app --access-logfile -
