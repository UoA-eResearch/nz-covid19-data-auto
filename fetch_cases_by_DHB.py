#!/usr/bin/env python3

import requests
import time
import re
from bs4 import BeautifulSoup
import csv

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

table = soup.find("caption", string=re.compile("Total cases by location")).parent
headers = []
for heading in table.find("thead").find_all("th"):
    if heading.text == "Location":
        headers.append("DHB")
    else:
        headers.append(heading.text)
rows = []
for row in table.find("tbody").find_all("tr"):
    row_list = []
    for col in row.find_all(["th", "td"]):
        if col.text == "\xa0":
            row_list.append("")
        else:
            row_list.append(col.get_text(strip=True).replace("ā", "a").replace(",", ""))
    if row_list:
        rows.append(row_list)
with open("cases_by_DHB.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)
    print("done")
