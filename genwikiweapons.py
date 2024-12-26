from urllib import request
from bs4 import BeautifulSoup
import pandas as pd

url = "https://genshin-impact.fandom.com/wiki/Weapon/List"
resp = request.urlopen(url)
data = resp.read()
soup = BeautifulSoup(data, 'html.parser')

# Locate the table containing the weapon list
table = soup.find("table")
trs = table.find_all("tr")

# Initialize lists to store the data
image, name, quality, base_atk, substat, passive = [], [], [], [], [], []

for tr in trs[1:]:  # Skip the header row
    tds = tr.find_all("td")
    
    if tds:
        # Extract image tag to get the 'alt' attribute (which contains the quality info)
        img_tag = tds[2].find("img")  # Assuming quality is in the third <td> (index 2)
        if img_tag and 'alt' in img_tag.attrs:
            quality_value = img_tag['alt'].strip()
            if quality_value in ["1 Star", "2 Stars"]:
                continue  # Skip rows with "1 Star" or "2 Stars"
        else:
            continue  # Skip rows with missing quality
        
        # Extract image URL from the first column
        img_column_tag = tds[0].find("img")
        if img_column_tag:
            img_url = img_column_tag.get('data-src', img_column_tag.get('src', ''))
        else:
            img_url = ''  # Fallback if no image is found
        image.append(img_url)
        
        # Extract weapon name and other details
        name.append(tds[1].text.strip())
        quality.append(quality_value)
        base_atk.append(tds[3].text.strip())
        substat.append(tds[4].text.strip())
        passive.append(tds[5].text.strip() if len(tds) > 5 else '')

# Create a DataFrame to organize the data
df = pd.DataFrame({
    "image": image,
    "name": name, 
    "quality": quality, 
    "base_atk": base_atk, 
    "substat": substat, 
    "passive": passive
})

# Output the DataFrame
print(df)

# Save the DataFrame to a CSV file
df.to_csv('weapons.csv', index=False)
