import requests
from bs4 import BeautifulSoup
import json


#Function for scrapping data from the given url with particular number of pages
def scraperFunction(url):
    prodArray = []
    targetURL = "https://www.amazon.in"

    #User Agents to prevent blocking of Ip
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }
    pages = 1
    while pages < 21:
        webContent = requests.get(url + "&page=" + str(pages), headers=headers)
        parsedWebPage = BeautifulSoup(webContent.text, "html.parser")

        for product in parsedWebPage.find_all("div", class_="s-result-item"):
            productUrl = product.find("a", href=True)
            if productUrl and "/dp/" in productUrl["href"]:
                productUrl = targetURL + productUrl["href"]
            else:
                continue

            productName = product.find(
                "span", class_="a-size-medium a-color-base a-text-normal")
            productPrice = product.find("span", class_="a-price-whole")
            productRating = product.find("span", class_="a-icon-alt")
            productReviewCount = product.find(
                "span", class_="a-size-base s-underline-text")

            if productName:
                productName = productName.text
            if productPrice:
                productPrice = productPrice.text.replace(",", "")
            if productRating:
                productRating = productRating.text.split(" ")[0]
            if productReviewCount:
                productReviewCount = productReviewCount.text[1:-1].replace(
                    ",", "")

            prodArray.append({
                "url": productUrl,
                "name": productName,
                "price": productPrice,
                "productRating": productRating,
                "reviews": productReviewCount
            })
        pages += 1
    return prodArray


finalURL = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
products = scraperFunction(finalURL)

#Writing to json file so that part 2 can read it and scrap more info about each product
with open("productList.json", "w") as file:
    json.dump(products, file, indent=4)