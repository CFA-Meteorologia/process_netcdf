from helpers import extract_tiff_from_var
from datetime import datetime
import shutil
import os
from config import get_config

temp_dir = get_config('temp_dir')

try:
    shutil.rmtree(temp_dir)
except FileNotFoundError:
    pass
os.mkdir(temp_dir)

extract_tiff_from_var(
    datetime.fromisoformat('2020-07-06 00:00:00'),
    datetime.fromisoformat('2020-07-07 00:00:00'),
    'T2',
)
