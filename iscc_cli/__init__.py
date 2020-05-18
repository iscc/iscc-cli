import iscc_cli.monkeys
import os
import click


__version__ = "0.9.9"
APP_NAME = "iscc-cli"
APP_DIR = click.get_app_dir(APP_NAME, roaming=False)
os.makedirs(iscc_cli.APP_DIR, exist_ok=True)
os.environ["TIKA_PATH"] = APP_DIR
os.environ["TIKA_LOG_PATH"] = APP_DIR
os.environ["TIKA_STARTUP_MAX_RETRY"] = "5"
os.environ["LOGURU_AUTOINIT"] = "False"


from iscc_cli.tika import tika

tika.log.disabled = True
