FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /webapp

# Install wkhtmltopdf
RUN apt-get update && apt-get install -y wkhtmltopdf

WORKDIR /webapp
COPY requirements.txt /webapp/
RUN pip install -r requirements.txt
COPY . /webapp/