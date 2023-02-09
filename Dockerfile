FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip install -r req.txt

COPY ./src .
COPY ./run.sh .

RUN chmod +x ./run.sh

ENTRYPOINT [ "./run.sh" ]