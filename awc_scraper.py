import pandas as pd
import json
import avwx
import random
from time import sleep
import plotly.express as px
from datetime import datetime, timezone
from urllib.request import urlretrieve
import gzip
import shutil
import os


cache_url = 'https://aviationweather.gov/data/cache/metars.cache.csv.gz'
cache_file = 'metar.cache.csv.gz'
color_key = {'VFR': 'green', 'MVFR': 'blue', 'IFR': 'red', 'LIFR': 'fuchsia'}


def get_current_time():
    now = datetime.now(timezone.utc)
    return now.strftime('%d%b%y, %H%MZ').upper()


def get_cache():
    urlretrieve(cache_url, cache_file)
    return None


def extract_cache():
    with gzip.open(cache_file, 'rb') as f_in:
        with open('metar.cache.csv', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    # Get rid of first five lines, load to dataframe
    airport_weather = pd.read_csv('metar.cache.csv', skiprows=5)
    return airport_weather


def compile_awc():
    get_cache()
    data = extract_cache()
    os.remove(f'/home/enzi/eMFmapper/{cache_file}')
    os.remove('/home/enzi/eMFmapper/metar.cache.csv')
    return data


def awc_mapper(airports: pd.DataFrame):
    report_time = get_current_time()
    report_title = f'Report generated at {report_time}'
    # Plotting results
    print('Displaying map')
    metar_map = px.scatter_geo(airports, lat='latitude', lon='longitude', color='flight_category',
                               color_discrete_map=color_key, hover_name='station_id', title=report_title)
    metar_map.update_geos(scope='usa')
    metar_map.show()
    return None
