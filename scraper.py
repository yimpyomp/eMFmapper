import pandas as pd
import json
import avwx
import random
from time import sleep


color_key = {'VFR': 'green', 'MVFR': 'blue', 'IFR': 'red', 'LIFR': 'fuchsia'}
icao_exclusion_list = ['KCWS', 'KEYQ']


def open_airport_json(filename):
    if '.json' not in filename:
        raise Exception('Data must be in JSON format')
    f = open(filename)
    raw_airports = json.load(f)
    return raw_airports


def parse_json(country, data_json):
    filtered_airports = []
    for entry in data_json:
        if data_json[entry]["country"] == country:
            filtered_airports.append([data_json[entry]["icao"], data_json[entry]["name"],
                                      data_json[entry]["lat"], data_json[entry]["lon"]])
    return filtered_airports


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


# Working, need a good way to reduce size of airport list
def get_flight_rules(airports):
    # Creating empty list to store flight rule values
    current_rules = []
    # Empty list to store colors corresponding to current rules
    color_codes = []
    # Iterating through list of airports
    for entry in airports:
        airport = entry[0]
        print(f'Retrieving data for {airport}')
        # Creating a METAR object and fetching current data
        try:
            current_report = avwx.Metar(airport)
            current_report.update()
            try:
                # Adding current flight rules to list
                current_rules.append(current_report.data.flight_rules)
                # Storing rule in variable for color list
                current_field_condition = current_report.data.flight_rules
                # Populating empty color list based on current rules
                color_codes.append(color_key[current_field_condition])
                if len(current_rules) % 15 == 0:
                    sleep(2)
            except AttributeError:
                pass
        except avwx.exceptions.BadStation:
            pass


    print('Flight rules complete')
    # Returning list of flight rules
    return current_rules, color_codes


def randomize_report(airport_list, group_size):
    upper_limit = len(airport_list)
    randomized_indices = []
    while len(randomized_indices) < group_size:
        randomized_indices.append(random.randrange(upper_limit))
    random_fields = [airport_list[i] for i in randomized_indices]
    return random_fields


# Currently unused.
def cache_results(airports):
    list_size = len(airports)
    current_rules, color_codes = [], []
    for i in range(0, list_size, 15):
        print(f'Retrieving data up to airport {i}')
        cache_rules, cache_rules = get_flight_rules(airports[:i])
        current_rules += cache_rules
        color_codes += color_codes
        sleep(2)
    print(f'Cache complete')
    return current_rules, color_codes



