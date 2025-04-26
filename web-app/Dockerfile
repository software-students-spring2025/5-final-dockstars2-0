FROM python:3.10-slim

# install pipenv
RUN pip install pipenv

# set working directory
WORKDIR /app

# copy pipenv files
COPY Pipfile Pipfile.lock ./

# install dependencies
RUN pipenv install --deploy --system

# add files from rest of app
ADD . /app

# run on port 5000
EXPOSE 8080

# Run app.py when the container launches
CMD ["python", "app.py"]