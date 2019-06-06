import os
import click

os.environ["TIKA_VERSION"] = "1.21"
__version__ = "0.5.0"

APP_NAME = "iscc-cli"
APP_DIR = click.get_app_dir(APP_NAME)
