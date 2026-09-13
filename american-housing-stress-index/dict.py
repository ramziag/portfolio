import requests as rq
from dotenv import load_dotenv
from os import getenv
load_dotenv()


my_key = getenv('api_key')

url = 'https://api.census.gov/data/2024/acs/acs5/groups'

my_list = ['B25091']
payload = {'key': my_key}

for x in my_list:
    r = rq.get(f'{url}/{x}.json', params = payload)
    data = r.json()
    print(str(data['variables'].keys()))

