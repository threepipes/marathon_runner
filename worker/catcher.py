"""
暫定版submission
flaskとかで作り直す
"""
import os
import time
import datetime
import shutil
from logging import getLogger, DEBUG, StreamHandler

import runner

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(DEBUG)


NEW_FILE_DIR = 'data/'
TARGET_DIR = 'archive/'
EXEC_COMMAND = 'node'
SLEEP_TIME = 5

def catcher(filename: str):
    logger.info('catch: ' + filename)
    timestamp = datetime.datetime.now().strftime('%y%m%d_%H%M%S')

    # move new file
    new_filename = f'{timestamp}_{filename}'
    filepath = NEW_FILE_DIR + filename
    new_filepath = TARGET_DIR + new_filename
    shutil.move(filepath, new_filepath)

    # create runner option
    command = f'{EXEC_COMMAND} {new_filepath}'
    label = new_filename
    run_num = 10
    runner.runner(command, run_num, label)
    logger.info('finish push: ' + filename)


def check_update() -> str:
    path_list = os.listdir(NEW_FILE_DIR)
    if len(path_list) > 0:
        return path_list[0]
    else:
        return ''

def main():
    while True:
        time.sleep(SLEEP_TIME)
        try:
            new_file = check_update()
            if new_file:
                catcher(new_file)
        except KeyboardInterrupt:
            logger.info('exit')
            break
        except Exception as e:
            logger.error(e)

if __name__ == '__main__':
    main()