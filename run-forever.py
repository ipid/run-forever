"""
Simple tool for deploying server applications.
Run specific command, and run again if it stops.
"""

import argparse
import logging
import subprocess
from logging.handlers import RotatingFileHandler
from time import sleep
from traceback import format_exc

DEFAULT_SLEEP_BEFORE_RESTART = 15
DEFAULT_LOG_FILE = 'log-run-forever.log'

argpar = argparse.ArgumentParser(
    prog='run-forever.py',
    description='Run specific command, and run again if it stops.',
)
argpar.add_argument(
    '--sleep', action='store',
    default=DEFAULT_SLEEP_BEFORE_RESTART, type=int,
    help=f'Seconds to sleep before restart. Default {DEFAULT_SLEEP_BEFORE_RESTART}.'
)
argpar.add_argument(
    '--log-file', action='store',
    default=DEFAULT_LOG_FILE, type=str,
    help=f'Name of log file. Default {DEFAULT_LOG_FILE}.'
)
argpar.add_argument(
    'command', type=str, default='', nargs='*',
    help='The command to run and restart.'
)


def run_command_once(cmd: str) -> int:
    """
    Run given command once (with a shell), wait till it finishes and return its status code.
    Stdout of the given command will be redirected to file_obj.

    :param cmd: The specific command
    :param file_obj: File object
    :return: Status code
    """
    logging.debug(f'Run command:「{cmd}」')

    proc = subprocess.Popen(cmd, shell=True)
    ret_code = int(proc.wait())
    return ret_code


def main():
    args = argpar.parse_args()

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(args.log_file, maxBytes=64 * 1024 * 1024,
                                backupCount=1, encoding='utf-8'),
        ],
    )
    cmd = ' '.join(args.command)

    while True:
        ret_code = None
        try:
            ret_code = run_command_once(cmd)
        except:
            logging.error(format_exc())

        if ret_code is not None:
            logging.debug(f'No Python exceptions was thrown. Status code: {ret_code}')

        sleep(args.sleep)


if __name__ == '__main__':
    main()
