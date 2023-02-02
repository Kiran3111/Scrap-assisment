import requests
import csv
from bs4 import BeautifulSoup
import json
import time
import random

urls = []

#Reading urls scrapped from part 1 so that more info can be scrapped
with open('productList.json') as file:
    data = json.load(file)

for item in data:
    value = item['url']
    urls.append(value)
    if len(urls) == 200:
        break

#Function to scrap Manufacturer from the website
def findManufacturer(content):
    manufacturer = ""
    table = content.find(
        "table", attrs={"id": "productDetails_techSpec_section_1"})
    if table:
        for tr in table.find_all("tr"):
            if tr.find("th").text.strip() == "Manufacturer":
                manufacturer = tr.find("td").text.strip()
                break
    else:
        detail = content.find("div", attrs={"id": "detailBullets_feature_div"})
        for li in detail.find_all('li'):
            span = li.find('span', {'class': 'a-text-bold'})
            if span and "Manufacturer" in span.text.strip() and "By Manufacturer" not in span.text.strip():
                manufacturer = li.find('span', {'class': None}).text.strip()
                if manufacturer != "No" or manufacturer != "Yes":
                    break
    return manufacturer

def getASIN(content):
    asin = ""
    table = content.find(
        "table", attrs={"id": "productDetails_techSpec_section_1"})
    if table:
        for tr in table.find_all("tr"):
            if tr.find("th").text.strip() == "ASIN":
                manufacturer = tr.find("td").text.strip()
                break
    else:
        detail = content.find("div", attrs={"id": "detailBullets_feature_div"})
        for li in detail.find_all('li'):
            span = li.find('span', {'class': 'a-text-bold'})
            if span and "ASIN" in span.text.strip():
                asin = li.find('span', {'class': None}).text.strip()
                break
    return asin

#Function to scrap the Description of the project from the website
def getDescription(content):
    bullet_points = content.find("div", {"id": "feature-bullets"})
    bullet_text = ""
    if bullet_points:
        for li in bullet_points.find_all("li"):
            bullet_text += li.text
    return bullet_text


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}
data = []
i = 1
for url in urls:
    print("Extracting product: "+str(i))
    i = i+1
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = BeautifulSoup(response.text, "html.parser")
        asin = getASIN(content)
        manufacturer = findManufacturer(content)
        description = getDescription(content)

        product_data = {
            "Description": description,
            "ASIN": asin,
            "Product Description": description,
            "Manufacturer": manufacturer.replace("\u200e", "")
        }
        data.append(product_data)
    else:
        delay = random.uniform(2, 5)
        time.sleep(delay)

#Writing all the data to csv file
with open("products.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file, fieldnames=["Description", "ASIN", "Product Description", "Manufacturer"])
    writer.writeheader()
    writer.writerows(data)

#Writing data to json file for examination
with open("products.json", "w") as file:
    json.dump(data, file, indent=4)