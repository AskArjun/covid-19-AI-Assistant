import os
import json
import requests
import pandas as pd
from datetime import date

# get data
covid_india = requests.get('https://api.covid19india.org/data.json').json()
covid_district = requests.get('https://api.covid19india.org/state_district_wise.json').json()


# total test cases
# total_tested_data = pd.DataFrame(covid_india['tested'])
def get_total_tested():
    total_tested = covid_india['tested'][len(covid_india['tested']) - 1]['totalsamplestested']

    if len(total_tested) <= 1:
        total_tested = covid_india['tested'][len(covid_india['tested']) - 2]['totalsamplestested']

    if len(total_tested) <= 1:
        total_tested = covid_india['tested'][len(covid_india['tested']) - 2]['totalsamplestested']

    if len(total_tested) <= 1:
        total_tested = covid_india['tested'][len(covid_india['tested']) - 3]['totalsamplestested']

    return total_tested


# prepare india level cases
total_india_data = pd.DataFrame(covid_india['cases_time_series'])


def get_india_cases(type_of_data):
    if type_of_data.lower() == 'confirmed':
        res = total_india_data['totalconfirmed'].values[len(total_india_data['totalconfirmed']) - 1]

    if type_of_data.lower() == 'deaths':
        res = total_india_data['totaldeceased'].values[len(total_india_data['totaldeceased']) - 1]

    if type_of_data.lower() == 'recovered':
        res = total_india_data['totalrecovered'].values[len(total_india_data['totalrecovered']) - 1]

    if type_of_data.lower() == 'active':
        res = str(int(total_india_data['totalconfirmed'].values[len(total_india_data['totalconfirmed']) - 1]) - \
              int(total_india_data['totaldeceased'].values[len(total_india_data['totaldeceased']) - 1]) - \
              int(total_india_data['totalrecovered'].values[len(total_india_data['totalrecovered']) - 1]))

    return res


# get cases state level

def get_state_cases(state_name, type_of_data):
    state_data = pd.DataFrame(covid_india['statewise'])

    if state_name == 'India':
        res = get_india_cases(type_of_data)
        today = date.today()
        last_updated = today.strftime("%d/%m/%Y")
        return res, last_updated

    # state_name = 'Andhra Pradesh'
    if type_of_data == 'confirmed':
        res = state_data.loc[state_data['state'].str.strip() == state_name, 'confirmed'].values[0]
        last_updated = state_data.loc[state_data['state'] == state_name, 'lastupdatedtime'].values[0]

    if type_of_data == 'deaths':
        res = state_data.loc[state_data['state'] == state_name, 'deaths'].values[0]
        last_updated = state_data.loc[state_data['state'] == state_name, 'lastupdatedtime'].values[0]

    if type_of_data == 'recovered':
        res = state_data.loc[state_data['state'] == state_name, 'recovered'].values[0]
        last_updated = state_data.loc[state_data['state'] == state_name, 'lastupdatedtime'].values[0]

    if type_of_data == 'active':
        res = state_data.loc[state_data['state'] == state_name, 'active'].values[0]
        last_updated = state_data.loc[state_data['state'] == state_name, 'lastupdatedtime'].values[0]

    return res, last_updated


# get district level information


def get_district_data(district_name, type_of_data):
    state = list()
    district = list()
    active = list()
    confirmed = list()
    deceased = list()
    recovered = list()

    for s in covid_district.keys():
        for dis in covid_district[s]['districtData'].keys():
            state.append(s)
            district.append(dis)
            active.append(covid_district[s]['districtData'][dis]['active'])
            confirmed.append(covid_district[s]['districtData'][dis]['confirmed'])
            deceased.append(covid_district[s]['districtData'][dis]['deceased'])
            recovered.append(covid_district[s]['districtData'][dis]['recovered'])

    district_data = pd.DataFrame(
        {'State': state, 'District': district, 'Confirmed': confirmed, 'Active': active, 'Deceased': deceased,
         'Recovered': recovered})

    if type_of_data == 'confirmed':
        res = district_data.loc[district_data['District'] == district_name, 'Confirmed'].values[0]

    if type_of_data == 'active':
        res = district_data.loc[district_data['District'] == district_name, 'Active'].values[0]

    if type_of_data == 'deaths':
        res = district_data.loc[district_data['District'] == district_name, 'Deceased'].values[0]

    if type_of_data == 'recovered':
        res = district_data.loc[district_data['District'] == district_name, 'Recovered'].values[0]

    return res
