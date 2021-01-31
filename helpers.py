from netCDF4 import Dataset
from wrf import getvar, geo_bounds
from os import path
from datetime import timedelta
from config import get_config
from serializer import to_serializable
import json


def read_var(netcdf_file_path, var_name):
    v = getvar(Dataset(netcdf_file_path), var_name)

    bounds = geo_bounds(v)
    bottom_left = bounds.bottom_left
    top_right = bounds.top_right

    east = top_right.lon
    west = bottom_left.lon
    north = top_right.lat
    south = bottom_left.lat

    return {
        "bounds": {
            "west": west,
            "east": east,
            "north": north,
            "south": south
        },
        "projection": "EPSG:4326",
        "data": v.values[::-1].tolist(),
    }


def get_file_names(netcdf_base_path, start_date, end_date, domain, time_interval=timedelta(hours=3)):
    current_date = start_date
    files = []

    while current_date <= end_date:
        formatted_date = current_date.strftime('%Y-%m-%d_%H:%M:%S')
        files.append(
            {
                "path": path.join(netcdf_base_path, f'wrfout_{domain}_{formatted_date}'),
                "date": current_date.isoformat()
            }
        )
        current_date = current_date + time_interval

    return files

def send_new_variables(start_date, end_date, var_name, domain, rabbit_mq_channel):
    netcdf_base_path = get_config('data_dir')

    file_names = get_file_names(
        path.join(path.join(netcdf_base_path, domain), domain),
        start_date, end_date, domain
    )

    for file in file_names:
        var = read_var(file['path'], var_name)

        rabbit_mq_channel.basic_publish(
            exchange=get_config('rabbitmq.exchange'),
            routing_key='',
            body=json.dumps({
                "bounds": var['bounds'],
                "data": var['data'],
                "projection": var['projection'],
                "domain": domain,
                "date": file['date'],
                "var": var_name
            }, default=to_serializable)
        )
