import configparser
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

cfg = configparser.ConfigParser()
cfg.read(project_root.joinpath('config.ini'))
