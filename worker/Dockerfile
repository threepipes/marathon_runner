# syntax = docker/dockerfile:experimental
FROM python:3.8

RUN --mount=type=cache,target=/var/cache/apt/ \
    apt update -y && \
    apt upgrade -y && \
    apt install -y sqlite3 curl software-properties-common \
    # to use optuna
    make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev liblapack-dev gfortran && \
    # to use node
    curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    apt -y install nodejs

WORKDIR /app/worker/
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# TODO: make python script to use settings.cfg
RUN ./create_db.sh /app/worker/test.db

CMD [ "python", "worker.py" ]
