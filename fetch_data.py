import requests
import pandas as pd
import json

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
        params["filter"] = json.dumps(filter_json)  # lad requests håndtere URL-kodning
    if sort:
        params["sort"] = sort  # ikke ekstra encode
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
