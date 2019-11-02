"""
暫定版submission
flaskとかで作り直す
"""
import os
import time
import datetime
import shutil
from logging import getLogger, DEBUG, StreamHandler
from configparser import ConfigParser

import runner

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(DEBUG)

config = ConfigParser()
config.read('settings.cfg')

catcher_configs = config.get('catcher', {})
NEW_FILE_DIR = catcher_configs.get('input_file_dir', '')
TARGET_DIR = catcher_configs.get('archive_file_dir', '')
SLEEP_TIME = int(catcher_configs.get('sleep_time', 5))

EXEC_COMMAND = 'node' # TODO: set by args or file ext


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
    return path_list[0] if len(path_list) > 0 else ''


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
