FROM python:3.8-alpine

RUN apk update && \
    apk upgrade && \
    apk add --no-cache --update sqlite nodejs

WORKDIR /app/
COPY . .

RUN ./create_db.sh /app/test.db

RUN pip install -r requirements.txt
CMD [ "python", "worker.py" ]
