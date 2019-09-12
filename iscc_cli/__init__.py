import os
import click

os.environ["TIKA_VERSION"] = "1.22"
__version__ = "0.7.0"

APP_NAME = "iscc-cli"
APP_DIR = click.get_app_dir(APP_NAME)
