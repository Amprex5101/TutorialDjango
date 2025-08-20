import os
import environ
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


current_path = Path(__file__).resolve().parent.parent
site_root = current_path
env_file = site_root / '.env'
print(current_path)
if env_file.exists():
    env = environ.Env()
    environ.Env.read_env(env_file=env_file)


def env(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)
