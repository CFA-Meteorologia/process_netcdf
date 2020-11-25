from netCDF4 import Dataset
from wrf import getvar, geo_bounds
from os import path, access, makedirs, F_OK
from datetime import datetime, timedelta
import rasterio


def readVars(netcdfFilePath, varName, outputDir='./temp'):
    v = getvar(Dataset(netcdfFilePath), varName)

    bounds = geo_bounds(v)
    bottom_left = bounds.bottom_left
    top_right = bounds.top_right

    east = top_right.lon
    west = bottom_left.lon
    north = top_right.lat
    south = bottom_left.lat

    width = v.shape[1]
    height = v.shape[0]

    transform = rasterio.transform.from_bounds(west, south, east, north, width, height)

    if not access(outputDir, F_OK):
        makedirs(outputDir)

    with rasterio.open(
            path.join(outputDir, path.basename(netcdfFilePath)),
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=v.dtype,
            crs=4326,
            transform=transform
    ) as dst:
        dst.write(v.values[::-1], 1)


def get_file_names(netcdf_base_path, start_date, end_date, domain, time_interval=timedelta(hours=3)):
    current_date = start_date
    files = []

    while current_date <= end_date:
        formatted_date = current_date.strftime('%Y-%m-%d_%H:%M:%S')
        files.append(
            path.join(netcdf_base_path, f'wrfout_{domain}_{formatted_date}')
        )
        current_date = current_date + time_interval

    return files

def extract_tiff_from_var(netcdf_base_path, start_date, end_date, var_name, temp_dir):
    domains = ['d01', 'd02', 'd03']
    for d in domains:
        file_names = get_file_names(
            path.join(path.join(netcdf_base_path, d ), d),
            start_date, end_date, d
        )
        for file in file_names:
            readVars(file, var_name, temp_dir)