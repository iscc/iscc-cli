import os
import click

__version__ = "0.8.1"

APP_NAME = "iscc-cli"
APP_DIR = click.get_app_dir(APP_NAME, roaming=False)

os.environ["TIKA_VERSION"] = "1.22"
os.environ["TIKA_PATH"] = APP_DIR
