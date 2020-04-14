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
df = pd.read_excel(link, skiprows=3, sheet_name=None)
for k,v in df.items():
    v["Case Type"] = k
df = pd.concat(df.values())
cols = df.columns[~df.columns.str.startswith('Unnamed:')]
df = df[cols]
df["Age group"] = df["Age group"].str.strip()
df["Last country before return"] = df["Last country before return"].str.strip()
df = df.sort_values(by=list(df.columns), ascending=False)
df.to_json("data.json", orient="records", indent=4)
df.to_csv("data.csv", index=False)