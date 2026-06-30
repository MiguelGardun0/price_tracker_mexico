import requests
from bs4 import BeautifulSoup
import json

HEADERS =  {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }

#URL = "https://www.mercadolibre.com.mx/panini-manga-mexico--berserk-13/up/MLMU587209408?matt_tool=28238160"

def scrape_product_meli(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", type="application/ld+json")
        data = json.loads(script_tag.string)

        name = data["name"]
        price = data["offers"]["price"]
        availability = data["offers"]["availability"]
        valid_until = data["offers"]["priceValidUntil"]

        return { "product_name": name, 
                'product_price': price, 
                'product_availability': (False if availability == 'https://schema.org/OutOfStock' else True), 
                'offer_valid_until': valid_until, 
                "marketplace": "MercadoLibre", 
                "url": url }

    elif response.status_code == 403:
        return "Blocked — site rejected the request"
    elif response.status_code == 429:
        return "Rate limited — too many requests"
    else:
        return f"Unexpected status: {response.status_code}"



