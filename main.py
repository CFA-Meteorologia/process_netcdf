from helpers import update_geoserver_layer
from datetime import datetime
import shutil
import os
from config import get_config
from geoserver.catalog import Catalog

temp_dir = get_config('temp_dir')

try:
    shutil.rmtree(temp_dir)
except FileNotFoundError:
    pass
os.mkdir(temp_dir)

geoserver = Catalog(
    get_config('geoserver.restUrl'),
    get_config('geoserver.user'),
    get_config('geoserver.password'),
)


# create workspace if not exists, a workspace is mandatory to work with geoserver
workspace_name = get_config('geoserver.workspace')
workspace = geoserver.get_workspace(workspace_name)
if workspace is None:
    geoserver.create_workspace(
        workspace_name,
        get_config('geoserver.hostUrl') + workspace_name
    )
    geoserver.reload()

update_geoserver_layer(
    datetime.fromisoformat('2020-07-06 00:00:00'),
    datetime.fromisoformat('2020-07-07 00:00:00'),
    'T2',
    'd03',
    geoserver,
)
