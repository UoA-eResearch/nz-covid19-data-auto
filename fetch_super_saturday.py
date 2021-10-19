#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
import pandas as pd

import requests_cache
requests_cache.install_cache('cache')

url = "https://web.archive.org/web/20211015191851mp_/https://covid19.govt.nz/covid-19-vaccines/how-to-get-a-covid-19-vaccination/super-saturday/"
print(f"Fetching {url}")
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")
accordions = soup.find_all("accordion")
data = json.loads(accordions[1][":initial-list"])["accordionItems"]
dfs = []
for item in data:
    df = pd.read_html(item["answer"], header=0)[0]
    df.columns = ["Address", "Opening hours"]
    df["location"] = item["question"]
    df["Event description"] = "Pacific vaccination events"
    dfs.append(df)

links = soup.find(id="what-is-happening-around-the-country").parent.find_all("a", href=True)
for link in links:
    url = f"https://web.archive.org/{link['href']}"
    print(f"Fetching {url}")
    response = requests.get(url)
    try:
        plain_dfs = pd.read_html(response.text, header=0)
        print(f"Found {len(plain_dfs)} plain tables on the page")
        if plain_dfs and "super-accessible-vaccination-centres" in response.text:
            plain_dfs[-1]["Event description"] = "Super accessible vaccination centres"
        print(plain_dfs)
        for df in plain_dfs:
            df["page"] = link.text
            dfs.append(df)
    except Exception as e:
        print(e)
        pass
    
    soup = BeautifulSoup(response.text, "lxml")
    accordions = soup.find_all("accordion")
    print(f"Found {len(accordions)} accordions")
    if accordions:
        data = json.loads(accordions[0][":initial-list"])["accordionItems"]
        print(f"Found {len(data)} items")
        for item in data:
            df = pd.read_html(item["answer"], header=0)[0]
            df["location"] = item["question"]
            df["page"] = link.text
            dfs.append(df)
df = pd.concat(dfs, sort=False)
cols = df.columns[~df.columns.str.startswith('Unnamed:')]
df = df[cols]
print(df)
df.to_csv("vaccinations/super_saturday.csv", index=False)