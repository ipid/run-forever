"""
永久运行某个命令，在其结束后自动重启，并将 stdout
"""

import logging
import subprocess
import sys
from time import sleep
from traceback import format_exc

SLEEP_BEFORE_RESTART = 30
LOG_FILE = 'log-run-forever.log'
STDOUT_FILE = 'std(out,err)-run-forever.log'

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
    ],
)


def run_command_once(cmd: str, file_obj) -> int:
    """
    在终端中运行某个命令一次，将其输出放入文件对象 file_obj 中。
    返回命令的返回码。

    :param cmd: 要运行的命令
    :param file_obj: 文件对象
    :return: 命令运行的状态码
    """
    logging.debug(f'运行命令：「{cmd}」')

    proc = subprocess.Popen(cmd, stdout=file_obj, stderr=file_obj, shell=True)
    ret_code = int(proc.wait())
    return ret_code


def main():
    # run-forever.py 只有一个参数
    if len(sys.argv) != 2:
        print('Command must be passed in within one argument.\n'
              'Please add a pair of quotation mark around your command.')
        return

    cmd = sys.argv[-1]

    # 打开 stdout 文件，开始循环
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
            logging.debug(f'run_command_once 未出现异常。命令返回码：{ret_code}')

        sleep(SLEEP_BEFORE_RESTART)


if __name__ == '__main__':
    main()
