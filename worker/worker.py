import os
import redis
import rq
from logging import basicConfig, INFO

REDIS_URL = os.getenv('RQ_REDIS_URL')


def logging_config():
    # TODO: read from file
    _format = '[%(asctime)s %(levelname)s %(name)s]: %(message)s'
    basicConfig(level=INFO, format=_format)


def main():
    with rq.Connection(redis.from_url(REDIS_URL)):
        worker = rq.Worker(['default'])
        worker.work()


if __name__ == '__main__':
    logging_config()
    main()
