import os
import redis
import rq
from logging import basicConfig, INFO


def logging_config():
    _format = '[%(asctime)s %(levelname)s %(name)s]: %(message)s'
    basicConfig(level=INFO, format=_format)


def main():
    with rq.Connection(redis.from_url(os.environ.get('RQ_REDIS_URL'))):
        worker = rq.Worker(['default'])
        worker.work()


if __name__ == '__main__':
    logging_config()
    main()
