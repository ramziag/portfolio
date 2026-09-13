import requests as rq
import pandas as pd
from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from pprint import pp
load_dotenv()

# variables
p = Path('.')
url = 'http://api.census.gov/data/2024/acs/acs5'
var_url = 'https://api.census.gov/data/2024/acs/acs5/variables'
my_key = getenv('api_key')
my_vars = "NAME,B25001_001E,B25002_001E,B25002_003E,B25003_001E,B25003_002E,B25003_003E,B19013_001E,B25070_001E,B25070_002E,B25070_003E,B25070_004E,B25070_005E,B25070_006E,B25070_007E,B25070_008E,B25070_009E,B25070_010E,B25070_011E,B25091_001E,B25091_002E,B25091_003E,B25091_004E,B25091_005E,B25091_006E,B25091_007E,B25091_008E,B25091_009E,B25091_010E,B25091_011E,B25091_012E,B25091_013E,B25091_014E,B25091_015E,B25091_016E,B25091_017E,B25091_018E,B25091_019E,B25091_020E,B25091_021E,B25091_022E,B25091_023E"
state_fips = {
    "01": "Alabama",
    "02": "Alaska",
    "04": "Arizona",
    "05": "Arkansas",
    "06": "California",
    "08": "Colorado",
    "09": "Connecticut",
    "10": "Delaware",
    "11": "District of Columbia",
    "12": "Florida",
    "13": "Georgia",
    "15": "Hawaii",
    "16": "Idaho",
    "17": "Illinois",
    "18": "Indiana",
    "19": "Iowa",
    "20": "Kansas",
    "21": "Kentucky",
    "22": "Louisiana",
    "23": "Maine",
    "24": "Maryland",
    "25": "Massachusetts",
    "26": "Michigan",
    "27": "Minnesota",
    "28": "Mississippi",
    "29": "Missouri",
    "30": "Montana",
    "31": "Nebraska",
    "32": "Nevada",
    "33": "New Hampshire",
    "34": "New Jersey",
    "35": "New Mexico",
    "36": "New York",
    "37": "North Carolina",
    "38": "North Dakota",
    "39": "Ohio",
    "40": "Oklahoma",
    "41": "Oregon",
    "42": "Pennsylvania",
    "44": "Rhode Island",
    "45": "South Carolina",
    "46": "South Dakota",
    "47": "Tennessee",
    "48": "Texas",
    "49": "Utah",
    "50": "Vermont",
    "51": "Virginia",
    "53": "Washington",
    "54": "West Virginia",
    "55": "Wisconsin",
    "56": "Wyoming"
}
my_var_list = [x for x in my_vars.split(',')]

for k, v in state_fips.items(): 
    print(f"Now obtaining data for {v}:")
    payload = {
        'get': my_vars,
        'for': 'tract:*',
        'in': f'state:{k} county:*',
        'key': my_key
        }
    r = rq.get(url, params = payload)
    data = r.json()
    df = pd.DataFrame(data)
    df.columns = df.iloc[0]
    df = df[0:]

    var_data_keys = []
    var_data_values = []

    for var in my_var_list:
        r = rq.get(f'{var_url}/{var}.json')
        var_data = r.json()
        var_data_keys.append(var_data['name'])
        print(f"{var_data['name']} appended to list.")
        if len(var_data['concept']) > 100:
            var_data_values.append(f"{var_data['name']}({var_data['label']})")
        else:
            var_data_values.append(f"{var_data['name']}({var_data['label']} - {var_data['concept']})")
        print(f"{var_data['name']}({var_data['label']} - {var_data['concept']}) appended to list.")
    var_data_dict = dict(zip(var_data_keys, var_data_values))
    df.rename(columns=var_data_dict, inplace=True)
    df.drop(index = 0, inplace=True)
    output_path = p/('output')/f'{v}_data_tracts.csv'
    df.to_csv(output_path)
    print(f"Successfully output to file {output_path}")

