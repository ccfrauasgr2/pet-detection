FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# port where the Django app runs
EXPOSE 8000

COPY . .

CMD ["python", "manage.py", "runserver", "8000"]