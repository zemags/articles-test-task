FROM python:3.8

WORKDIR /usr/src/app

# prevent writing pyc and buffering stdout, stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . /usr/src/app/