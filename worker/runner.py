import os
import sqlite3
import datetime
import redis
import argparse
import subprocess
from rq import Queue
from logging import getLogger, DEBUG, StreamHandler

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(DEBUG)

DB = '/app/test.db'
TABLE = 'worker'
REDIS_URL = os.getenv('RQ_REDIS_URL')


def save_score(idx: int, i: int, score: int, label: str):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    sql = f"""
        insert into {TABLE} (id, label, num, result, create_datetime)
            values ({idx}, '{label}', {i}, {score}, datetime('now', 'localtime'))
    """
    logger.debug(sql)
    cur.execute(sql)
    con.commit()
    con.close()


def execute(idx: int, i: int, command: str, label: str):
    logger.debug(f'executing: {command} {i}')
    output = subprocess.check_output(command.split())
    logger.debug(output)
    save_score(idx, i, int(output), label)
    logger.info(f'fin command: {i}')


def runner(command: str, run_num: int=3, label: str=''):
    """
        command: 実行すると、実行後にスコアが返ることを前提としている
        run_num: 実行回数 (optional)
        label: コマンド名 バージョン名などプログラムを識別する名称 (optional)
    """
    logger.debug(f'executing: {command} in {run_num} times')
    timestamp = int(datetime.datetime.now().timestamp())
    q = Queue(connection=redis.from_url(REDIS_URL), default_timeout=3600)
    for i in range(run_num):
        q.enqueue(execute, args=(timestamp, i, command, label))
    # TODO: enque a task to check finish all tasks


def main(args):
    command = args.command
    run_num = int(args.run_num)
    label = args.label
    runner(command, run_num, label)
