FROM python:3.12-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --system

COPY . .

CMD ["python", "app.py"]
