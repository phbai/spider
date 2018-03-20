FROM python:3-alpine
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip \
    && pip install -r requirements.txt