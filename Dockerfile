FROM python:3.10.12

WORKDIR /incident
COPY requirements.txt /incident/
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD python manage.py runserver