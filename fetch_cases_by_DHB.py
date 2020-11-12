#!/usr/bin/env python3

import requests
import time
import re
from bs4 import BeautifulSoup
import csv
from util import html_table_to_df

url = "https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-data-and-statistics/covid-19-current-cases"
url += f"?{time.time()}"
r = requests.get(url, timeout=5)
print("Got data")
soup = BeautifulSoup(r.content)

search_string = "Last updated"
last_modified = soup.find("p", text=re.compile(search_string)).text
last_modified = last_modified[last_modified.find(search_string) + len(search_string):].strip(". ").replace(u'\xa0', " ") # nbsp
with open("last_modified.txt", "w") as f:
    f.write(last_modified)
print(last_modified)

df = html_table_to_df(soup, "Total cases by location")
df.columns = ["DHB", "Active", "Recovered", "Deceased", "Total", "Change in last 24 hours"]
df.to_csv("cases_by_DHB.csv", index=False)
print(df)