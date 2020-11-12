import pandas as pd
import re

def html_table_to_df(soup, caption_string):
    table = soup.find("caption", string=re.compile(caption_string)).parent
    headers = []
    for heading in table.find("thead").find_all("th"):
        headers.append(heading.text.replace("*", ""))
    rows = []
    for row in table.find("tbody").find_all("tr"):
        row_list = []
        for col in row.find_all(["th", "td"]):
            row_list.append(col.get_text(strip=True).replace("ā", "a").replace(",", ""))
        if row_list:
            rows.append(row_list)
    return pd.DataFrame(rows, columns=headers)