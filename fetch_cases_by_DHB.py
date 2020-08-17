#!/usr/bin/env python3

import requests
import time
import re
from bs4 import BeautifulSoup
import csv

url = "https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases"
url += f"?{time.time()}"
r = requests.get(url)
soup = BeautifulSoup(r.content)

#with open("test.html") as f:
#    soup = BeautifulSoup(f.read())

table = soup.find("caption", string=re.compile("Total cases by DHB")).parent
headers = []
for heading in table.find("thead").find_all("th"):
    headers.append(heading.text)
rows = []
for row in table.find("tbody").find_all("tr"):
    row_list = []
    for col in row.find_all(["th", "td"]):
        if col.text == "\xa0":
            row_list.append("")
        else:
            row_list.append(col.text.replace("ā", "a").replace(",", "").replace("\n", ""))
    if row_list:
        rows.append(row_list)
with open("cases_by_DHB.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)
    print("done")
