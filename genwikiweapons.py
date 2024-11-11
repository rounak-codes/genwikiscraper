# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 14:48:16 2024

@author: rounak-codes
"""

from urllib import request
from bs4 import BeautifulSoup
import pandas as pd

url = "https://genshin-impact.fandom.com/wiki/Weapon/List"
resp = request.urlopen(url)
data = resp.read()
soup = BeautifulSoup(data, 'html.parser')
table = soup.find("table")
trs = table.find_all("tr")
name, quality, base_atk, substat, passive = [], [], [], [], []

for tr in trs[1:]: # Skip the header row
    tds = tr.find_all("td")
    if tds:
        name.append(tds[1].text.strip())
        quality.append(tds[2].text.strip())
        base_atk.append(tds[3].text.strip())
        substat.append(tds[4].text.strip())
        passive.append(tds[5].text.strip() if len(tds) > 5 else '')

df = pd.DataFrame({"name": name, "quality": quality, "base_atk": base_atk, 
                   "substat": substat, "passive": passive})
print(df)

df.to_csv('weapons.csv')