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

color_key = {'VFR': 'green', 'MVFR': 'blue', 'IFR': 'red', 'LIFR': 'fuchsia'}
icao_exclusion_list = ['KEYQ', 'KCWS']
# Marks whether any excluded airports have been found
exclusion_flag = False


def open_airport_json(filename):
    if '.json' not in filename:
        raise Exception('Data must be in JSON format')
    f = open(filename)
    raw_airports = json.load(f)
    return raw_airports


def parse_json(country, data_json, state_filters=None):
    filtered_airports = []
    if state_filters:
        state_filters = regex_scary(state_filters)
        for entry in data_json:
            if data_json[entry]["country"] == country and data_json[entry]["state"] in state_filters:
                filtered_airports.append([data_json[entry]["icao"], data_json[entry]["name"],
                                          data_json[entry]["lat"], data_json[entry]["lon"]])
    else:
        for entry in data_json:
            if data_json[entry]["country"] == country:
                filtered_airports.append([data_json[entry]["icao"], data_json[entry]["name"],
                                          data_json[entry]["lat"], data_json[entry]["lon"]])
    return filtered_airports


def regex_scary(filter_list):
    for element in filter_list:
        if ' ' in element:
            interim = ' '.split(element)
            filter_list.append('-'.join(interim))
        else:
            continue
    return filter_list


def filter_numbered_fields(airport_list):
    no_numbers_allowed = []
    for entry in airport_list:
        numerical_id = False
        for letter in entry[0]:
            if letter.isdigit():
                numerical_id = True
        if not numerical_id:
            no_numbers_allowed.append(entry)
    return no_numbers_allowed


def remove_closed(airport_list):
    final = [i for i in airport_list if i[0] not in icao_exclusion_list]
    return final


def get_current_time():
    now = datetime.now(timezone.utc)
    return now.strftime('%d%b%y, %H%MZ').upper()


# Working, need a good way to reduce size of airport list
def get_flight_rules(airports: list):
    """
    Retrieves current weather conditions of provided airports
    :param airports: Nested list of airports
    :return: Original nested list of airports with both current condition
    """
    global exclusion_flag
    # Iterating through list of airports, enumerate for pausing
    for count, entry in enumerate(airports):
        airport = entry[0]
        print(f'Retrieving data for {airport}')
        # Creating a METAR object and fetching current data
        try:
            current_report = avwx.Metar(airport)
            current_report.update()
            try:
                # Adding current flight rules to list
                entry.append(current_report.data.flight_rules)
                # Storing rule in variable for color list
                current_field_condition = current_report.data.flight_rules
                # Populating empty color list based on current rules
                entry.append(color_key[current_field_condition])
                if count % 15 == 0:
                    sleep(2)
            except AttributeError:
                pass
        except avwx.exceptions.BadStation:
            # Adding experimental code to attempt to create a list of fields that are closed
            exclusion_flag = True
            icao_exclusion_list.append(entry[0])
            pass
    print('Flight rules complete')
    if exclusion_flag:
        save_exclusion_list()
        print('Exclusion list updated')
    # Returning list of flight rules
    return airports


def randomize_report(airport_list, group_size):
    upper_limit = len(airport_list)
    randomized_indices = []
    while len(randomized_indices) < group_size:
        randomized_indices.append(random.randrange(upper_limit))
    random_fields = [airport_list[i] for i in randomized_indices]
    return random_fields


# This works now
def compile_data(airports_list):
    """
    Compiles list of airport data
    :param airports_list: Nested list of airports and related weather conditions
    :return: Pandas DataFrame containing airport information
    """
    airports_list = [i for i in airports_list if len(i) == 6]
    airport_weather = pd.DataFrame(airports_list, columns=['Identifier', 'Name', 'Lat', 'Lon', 'Condition', 'Color'])
    return airport_weather


def metar_mapper(airports: pd.DataFrame):
    report_time = get_current_time()
    report_title = f'Report generated at {report_time}'
    # Plotting results
    print('Displaying map')
    metar_map = px.scatter_geo(airports, lat='Lat', lon='Lon', color='Condition', color_discrete_map=color_key,
                               hover_name='Name', title=report_title)
    metar_map.update_geos(scope='usa')
    metar_map.show()
    return None


def save_exclusion_list():
    with open('excluded_fields', 'w') as f:
        for entry in icao_exclusion_list:
            f.writelines(entry + '\n')
        f.close()
    print(icao_exclusion_list)
    return None







