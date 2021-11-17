import os
import click

__version__ = "1.1.0b10"

APP_NAME = "iscc-cli"
APP_DIR = click.get_app_dir(APP_NAME, roaming=False)
if not os.path.exists(APP_DIR):
    os.makedirs(APP_DIR)
