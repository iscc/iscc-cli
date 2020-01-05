import iscc_cli.monkeys
import os
import click

__version__ = "0.9.0"

APP_NAME = "iscc-cli"
APP_DIR = click.get_app_dir(APP_NAME, roaming=False)
os.makedirs(iscc_cli.APP_DIR, exist_ok=True)

os.environ["TIKA_PATH"] = APP_DIR
