#!/usr/bin/env python3

import requests
import re
import os
from bs4 import BeautifulSoup
import pandas as pd
import time
from io import StringIO
from util import html_table_to_df
import sys

url = "https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-data-and-statistics/covid-19-vaccine-data"
url += f"?{time.time()}"
r = requests.get(url)
soup = BeautifulSoup(r.content)

link = soup.find("a", href=re.compile("xlsx"))
link = "https://www.health.govt.nz" + link["href"]
print(link)

force = False

if not force and os.path.isfile("last_vaccination_link.txt"):
    with open("last_vaccination_link.txt", "r") as f:
        last_link = f.read()
        if link == last_link:
            print("already done, exiting")
            exit(1)
with open("last_vaccination_link.txt", "w") as f:
    f.write(link)

r = requests.get(link)
sheets = pd.read_excel(r.content, sheet_name=None)
for k, df in sheets.items():
    print(k, df)
    df.to_csv(f"vaccinations/{k}.csv", index=False)