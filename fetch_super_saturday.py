#!/usr/bin/env python3

from pandas.core.frame import DataFrame
import requests
from bs4 import BeautifulSoup, element
import json
from pprint import pprint
import pandas as pd

from colorama import Fore, Back, Style

import requests_cache
requests_cache.install_cache('cache')

url = "https://web.archive.org/web/20211015191851mp_/https://covid19.govt.nz/covid-19-vaccines/how-to-get-a-covid-19-vaccination/super-saturday/"
print(f"{Fore.GREEN}Fetching {url}{Style.RESET_ALL}")
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
    page = link.text
    print(f"{Fore.CYAN}{page}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Fetching {url}{Style.RESET_ALL}")
    response = requests.get(url)
    plain_dfs = None
    try:
        plain_dfs = pd.read_html(response.text, header=0)
        print(f"Found {len(plain_dfs)} plain tables on the page")
        if plain_dfs and "super-accessible-vaccination-centres" in response.text:
            plain_dfs[-1]["Event description"] = "Super accessible vaccination centres"
        for df in plain_dfs:
            df["page"] = page
            dfs.append(df)
    except Exception as e:
        print(f"{Fore.RED}{e}{Style.RESET_ALL}")
    
    soup = BeautifulSoup(response.text, "lxml")
    accordions = soup.find_all("accordion")
    if len(accordions):
        print(f"Found {len(accordions)} accordions")
    else:
        print(f"{Fore.RED}No accordions found{Style.RESET_ALL}")
    if accordions:
        data = json.loads(accordions[0][":initial-list"])["accordionItems"]
        print(f"Found {len(data)} items")
        for item in data:
            df = pd.read_html(item["answer"], header=0)[0]
            df["location"] = item["question"]
            df["page"] = page
            dfs.append(df)
    else:
        link = soup.find("a", class_="external")
        if link and link.text.startswith(f"Super Saturday in {page}"):
            print(f"{Fore.YELLOW}Fetching external link: {link['href']}{Style.RESET_ALL}")
            response = requests.get(link['href'])
            soup = BeautifulSoup(response.text, "lxml")
            if page == "Northland":
                df = pd.read_html(response.text, header=0)[0]
                df.columns = ["Address", "Opening hours", "Event description"]
                df["page"] = page
                print(f"Found {len(df)} locations")
                dfs.append(df)
            elif page == "Otago":
                container = soup.find("div", class_="field-name-body")
                location = None
                locations = []
                for child in container.children:
                    if child.name == "p" and child.find("strong"):
                        location = child.get_text()
                    elif child.name == "ul":
                        for list_elem in child.children:
                            if list_elem.name == "li":
                                strings = list(list_elem.stripped_strings)
                                addr, time = strings[0].split(":", maxsplit=1)
                                desc = None
                                if len(strings) > 1:
                                    desc = strings[1]
                                locations.append({"Address": addr, "Opening hours": time, "Event description": desc, "location": location})
                df = pd.DataFrame(locations)
                df["page"] = page
                print(f"Found {len(df)} locations")
                dfs.append(df)
            elif page == "Taranaki":
                container = soup.select("div.col-xl-12 div.row")[0]
                locations = []
                for child in container.children:
                    if type(child) is element.Tag:
                        class_ = child["class"][0]
                        if class_ in ['col-sm-7', 'col-sm-9']:
                            strings = list(child.stripped_strings)
                            addr, time = strings[1].rsplit(", ", maxsplit=1)
                            location = strings[-1]
                            desc = None
                            if len(strings) > 3:
                                desc = strings[-2]
                            locations.append({"Address": addr, "Opening hours": time, "Event description": desc, "location": location})
                df = pd.DataFrame(locations)
                df["page"] = page
                print(f"Found {len(df)} locations")
                dfs.append(df)
            else:
                print(f"{Fore.RED}Don't know how to handle {page}{Style.RESET_ALL}")

df = pd.concat(dfs, sort=False)
cols = df.columns[~df.columns.str.startswith('Unnamed:')]
df = df[cols]
print(df)
df.to_csv("vaccinations/super_saturday.csv", index=False)