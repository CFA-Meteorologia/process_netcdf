from helpers import extract_tiff_from_var
from datetime import datetime

netcdfFilesPrefix = '/media/manuel/Data/insmet/latest'

extract_tiff_from_var(
    netcdfFilesPrefix,
    datetime.fromisoformat('2020-07-06 00:00:00'),
    datetime.fromisoformat('2020-07-07 00:00:00'),
    'T2'
)
