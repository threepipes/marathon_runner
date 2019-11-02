import os
import time
import sqlite3
import datetime
import redis
import argparse
import subprocess
from typing import List
from rq import Queue
from rq.job import Job
from logging import getLogger, DEBUG, StreamHandler
from configparser import ConfigParser

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(DEBUG)

config = ConfigParser
config.read('settings.cfg')

db_config = config.get('db', {})
DB = db_config.get('db_name', 'runner.db')
TABLE = db_config.get('table_name', 'results')
REDIS_URL = os.getenv('RQ_REDIS_URL')


def save_score(idx: int, i: int, score: int, label: str, param: str=''):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    # TODO: read scheme from settings
    sql = f"""
        insert into {TABLE} (id, label, param, num, result, create_datetime)
            values ({idx}, '{label}', '{param}', {i}, {score}, datetime('now', 'localtime'))
    """
    logger.debug(sql)
    cur.execute(sql)
    con.commit()
    con.close()


def execute(idx: int, i: int, command: str, label: str, param: str=''):
    logger.debug(f'executing: {command} {i}')
    output = subprocess.check_output(command.split())
    logger.debug(output)
    score = int(output)
    save_score(idx, i, int(output), label, param)
    logger.info(f'fin command: {i}')
    return score


def runner(command: str, run_num: int=3, label: str='', param: str='') -> List[Job]:
    """
        command: 実行すると、実行後にスコアが返ることを前提としている
        run_num: 実行回数 (optional)
        label: コマンド名 バージョン名などプログラムを識別する名称 (optional)
    """
    logger.debug(f'executing: {command} in {run_num} times')
    timestamp = int(datetime.datetime.now().timestamp())
    q = Queue(connection=redis.from_url(REDIS_URL), default_timeout=3600)
    tasks = [
        q.enqueue(execute, args=(timestamp, i, command, label, param), result_ttl=3600)
            for i in range(run_num)
    ]
    # TODO: enque a task to check finish all tasks

    return tasks


def check_finish_tasks(tasks: List[Job]):
    done_status = ('finished', 'failed')
    return all(map(lambda t: t.get_status() in done_status, tasks))


def run_with_wait(command: str, run_num: int=3, label: str='', param: str=''):
    tasks = runner(command, run_num, label, param)
    while True:
        if check_finish_tasks(tasks):
            break
        time.sleep(1)
    return tasks


def evaluation(command: str, run_num: int=3, label: str='', param: str='') -> int:
    tasks = run_with_wait(command, run_num, label, param)
    logger.debug([t.result for t in tasks])
    return sum(map(lambda t: t.result, tasks))


def main(args):
    command = args.command
    run_num = int(args.run_num)
    label = args.label
    runner(command, run_num, label)
