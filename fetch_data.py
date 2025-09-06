import datetime as dt
import requests
from datetime import date
import pandas as pd
import json
from nordpool import elspot

def fetch_data(dataset_name, start=None, end=None, columns=None, filter_json=None, sort=None, limit=1000, timezone=None):
    base_url = f"https://api.energidataservice.dk/dataset/{dataset_name}"
    params = {}

    if start:
        params["start"] = start
    if end:
        params["end"] = end
    if columns:
        params["columns"] = ",".join(columns)
    if filter_json:
        params["filter"] = json.dumps(filter_json)  
    if sort:
        params["sort"] = sort  
    if limit:
        params["limit"] = limit
    if timezone:
        params["timezone"] = timezone

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if "records" in data:
            return pd.DataFrame(data["records"])
        else:
            return pd.DataFrame(data)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"Unknown error: {e}")
    return pd.DataFrame()


#def fetch_nordpool_data(areas=["DK1","DK2"], resolution=60, days_back:int=None):
    end = date.today()
    prices_spot = elspot.Prices('EUR')
    
    #input validér
    if days_back:
        if not isinstance(days_back, int):
            raise ValueError("days_back must be an integer. days_back is how many days of day-ahead price history you want")
        
    for i in range(days_back + 1):
        fetch_date = end - dt.timedelta(days=i)
        prices = prices_spot.fetch(end_date=fetch_date, areas=areas, resolution=resolution)    

        rows = []
        for area, content in prices["areas"].items(): 
            for v in content["values"]:
                rows.append({
                    "HourUTC": v["start"], 
                    "PriceArea": area,
                    "SpotPriceEUR": v["value"]
                })
    
    df = pd.DataFrame(rows)
    df.sort_values(["HourUTC","PriceArea"], inplace=True)
    df.reset_index(drop=True, inplace=True) #reset index efter sort

    return df

    