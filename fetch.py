#!/usr/bin/env python3

import requests
import re
import os
from bs4 import BeautifulSoup
import pandas as pd
import time

url = "https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases/covid-19-current-cases-details"
url += f"?{time.time()}"
r = requests.get(url)
soup = BeautifulSoup(r.content)
#with open("test.html", "rb") as f:
#    soup = BeautifulSoup(f.read())
link = soup.find("a", href=re.compile("xlsx"))
link = "https://www.health.govt.nz" + link["href"]
print(link)
if os.path.isfile("last_link.txt"):
    with open("last_link.txt", "r") as f:
        last_link = f.read()
        if link == last_link:
            print("already done, exiting")
            exit(1)
with open("last_link.txt", "w") as f:
    f.write(link)
search_string = "Last updated"
last_modified = soup.find("p", text=re.compile(search_string)).text
last_modified = last_modified[last_modified.find(search_string) + len(search_string):].strip(". ").replace(u'\xa0', " ") # nbsp
with open("last_modified.txt", "w") as f:
    f.write(last_modified)
print(last_modified)
df = pd.read_excel(link, skiprows=2, sheet_name=None, skip_blank_lines=True)
for k,v in df.items():
    v["Case Type"] = k
df = pd.concat(df.values())
cols = df.columns[~df.columns.str.startswith('Unnamed:')]
df = df[cols]
df["Age group"] = df["Age group"].str.strip()
df["Last location before return"] = df["Last location before return"].str.strip()
df["Date of report"] = pd.to_datetime(df["Date notified of potential case"], dayfirst=True)
df = df.drop("Date notified of potential case", 1)
keys = list(df.keys())
keys.insert(0, keys.pop(keys.index("Date of report")))
df = df[keys]
df = df.sort_values(by=list(df.columns), ascending=False)
df.to_json("data.json", orient="records", indent=4)
df.to_csv("data.csv", index=False)
