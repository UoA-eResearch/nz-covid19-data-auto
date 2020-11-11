#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import pandas as pd
from io import StringIO
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)
driver.get("https://nzcoviddashboard.esr.cri.nz/")
driver.find_element_by_css_selector('div.selectize-input').click()
driver.find_element_by_css_selector('div.option[data-value="all"]').click() # Show all data
driver.find_element_by_css_selector('#overview-viewCurveData').click()
href = driver.find_element_by_css_selector('a[href*=session]').get_attribute("href")
session = href.split("/")[4]
route = driver.get_cookie("route")
cookie = "route=" + route["value"]
print(f"session={session}, cookie={cookie}")

time.sleep(3)

r = requests.get(f"https://nzcoviddashboard.esr.cri.nz/session/{session}/download/overview-downloadCurveData", headers={
    "Cookie": cookie
})

data = StringIO(r.text)
df = pd.read_csv(data, skiprows=3, skip_blank_lines=True)
df = df.dropna()
df.Date = pd.to_datetime(df.Date, dayfirst=True)
print(df)

df.to_csv("cases_by_DHB_over_time.csv", index=False)

driver.close()