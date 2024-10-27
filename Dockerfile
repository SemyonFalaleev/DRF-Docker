FROM python:3.12

EXPOSE 8000

WORKDIR /src

COPY requirements.txt /src/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /src/

RUN python manage.py makemigrations && python manage.py migrate

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]