"""
Simple tool for deploying server applications.
Run specific command, and run again if it stops.
"""

import logging
import subprocess
import sys
from time import sleep
from traceback import format_exc

SLEEP_BEFORE_RESTART = 30
LOG_FILE = 'log-run-forever.log'
STDOUT_FILE = 'std(out,err)-run-forever.log'

USAGE = f'''
Usage: {sys.argv[0]} <Your command>
Examples:
    {sys.argv[0]} fuck
    {sys.argv[0]} "ping -n 1 www.google.com"
'''

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
    ],
)


def run_command_once(cmd: str, file_obj) -> int:
    """
    Run given command once (with a shell), wait till it finishes and return its status code.
    Stdout of the given command will be redirected to file_obj.

    :param cmd: The specific command
    :param file_obj: File object
    :return: Status code
    """
    logging.debug(f'Run command:「{cmd}」')

    proc = subprocess.Popen(cmd, stdout=file_obj, stderr=file_obj, shell=True)
    ret_code = int(proc.wait())
    return ret_code


def main():
    # run-forever.py has only one parameter
    if len(sys.argv) != 2:
        print('Command must be passed in within one argument.\n'
              'Please add a pair of quotation mark around your command.')
        print(USAGE)
        return

    cmd = sys.argv[-1]

    f = open(STDOUT_FILE, 'w', encoding='utf-8')
    while True:
        ret_code = None
        try:
            ret_code = run_command_once(cmd, f)
        except:
            logging.error(format_exc())
        finally:
            f.flush()

        if ret_code is not None:
            logging.debug(f'No Python exceptions was thrown. Status code: {ret_code}')

        sleep(SLEEP_BEFORE_RESTART)


if __name__ == '__main__':
    main()
