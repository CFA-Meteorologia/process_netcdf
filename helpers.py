from netCDF4 import Dataset
from wrf import getvar, geo_bounds
from os import path
from datetime import timedelta
from config import get_config
from serializer import to_serializable
import json
import pika
from Variables import Variables


def read_var(netcdf_file, var_name):
    data_getter = Variables(netcdf_file)
    v = data_getter.get_var(var_name)

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


def send_new_variables(start_date, end_date, rabbit_mq_channel):
    netcdf_base_path = get_config('data_dir')

    domains = get_config('domains')

    for domain in domains:
        domain = f'd0{domain}'
        file_names = get_file_names(
            path.join(path.join(netcdf_base_path, domain), domain),
            start_date, end_date, domain
        )
        for file in file_names:
            process_netcdf_file(file['path'], rabbit_mq_channel, domain, file['date'])


def process_netcdf_file(file_path, rabbit_mq_channel, domain, date):

    variable_names = get_config('variables')

    file = Dataset(file_path)

    for var_name in variable_names:
        var = read_var(file, var_name)

        rabbit_mq_channel.basic_publish(
            exchange=get_config('rabbitmq.exchange'),
            routing_key='',
            body=json.dumps({
                "bounds": var['bounds'],
                "data": var['data'],
                "projection": var['projection'],
                "domain": domain,
                "date": date,
                "var": var_name
            }, default=to_serializable),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
