import os
import time

import pandas as pd
import requests as rq

TIMEOUT = 20  # seconds; never hang forever on a slow API

def save_data(all_props):
    save_path = 'data/zillow_data.csv'
    df = pd.DataFrame(all_props)
    df.to_csv(save_path, index=False)

def get_props_by_loc(URL, headers, querystring):
    props = []
    try:
        response = rq.get(URL, headers=headers, params=querystring, timeout=TIMEOUT)
        data = response.json()

        props.extend(data.get('props', []))
        total_pages = data.get('totalPages', 1)
        print(f'Total pages: {total_pages}')

        for page in range(2, total_pages+1):
            querystring['page'] = page
            print(f'Fetching page {page}...')

            response = rq.get(URL, headers=headers, params=querystring, timeout=TIMEOUT)
            page_data = response.json()
            page_props = page_data.get('props', [])
            props.extend(page_props)

            time.sleep(0.5)

    except Exception as e:
        print(f'The following exception happened:\n{e}')

    return props

def get_params():
    location = input('What city do you want to live in?\n')
    status_type = input('Do you want to buy or rent?\n')
    home_type = input('What type of property are you looking for?\n')
    return  {"location":f"{location}","status_type":f"{status_type}","home_type":f"{home_type}", "page": 1}

def main():
    api_key = os.environ.get("RAPIDAPI_KEY")
    if not api_key:
        raise SystemExit("Set the RAPIDAPI_KEY environment variable first.")
    URL = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
    headers = {
        "x-rapidapi-key": api_key,
		"x-rapidapi-host": "zillow-com1.p.rapidapi.com"
    }
    
    querystring = get_params()
    all_props = get_props_by_loc(URL, headers, querystring)
    save_data(all_props)

if __name__ == '__main__':
    main()

def search(form_data: dict):
    print(form_data.items())
    return