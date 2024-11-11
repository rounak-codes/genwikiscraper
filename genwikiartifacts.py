# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 15:02:52 2024

@author: rounak-codes
"""

from urllib import request
from bs4 import BeautifulSoup
import pandas as pd

url = "https://genshin-impact.fandom.com/wiki/Artifact/Sets"
resp = request.urlopen(url)
data = resp.read()
soup = BeautifulSoup(data, 'html.parser')
table = soup.find("table")
trs = table.find_all("tr")
name, quality, bonuses = [], [], []

for tr in trs[0:]: # Skip the header row
    tds = tr.find_all("td")
    if tds:
        name.append(tds[0].text.strip())
        quality.append(tds[1].text.strip())
        bonuses.append(tds[3].text.strip() if len(tds) > 3 else '')

df = pd.DataFrame({"name": name, "quality": quality, "bonuses": bonuses})
print(df)

df.to_csv('artifacts.csv')