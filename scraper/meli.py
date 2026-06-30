import requests
from bs4 import BeautifulSoup
import time
import json

#only works for offers atm

HEADERS =  {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }

URL = "https://www.mercadolibre.com.mx/birdman-falcon-performance-proteina-en-polvo-vegana-con-creatina-bcaas-y-enzimas-sin-lactosa-golden-vainilla-19kg/p/MLM18486368?pdp_filters=item_id%3AMLM1415283817"  

response = requests.get(URL, headers=HEADERS)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", type="application/ld+json")
    data = json.loads(script_tag.string)
    
    name = data["name"]
    price = data["offers"]["price"]
    availability = data["offers"]["availability"]
    valid_until = data["offers"]["priceValidUntil"]
    print(name, price, availability, valid_until)

elif response.status_code == 403:
    print("Blocked — site rejected the request")
elif response.status_code == 429:
    print("Rate limited — too many requests")
else:
    print(f"Unexpected status: {response.status_code}")

time.sleep(2)  

#https://www.mercadolibre.com.mx/natural-ultimate-omega-3-90-capsulas-nordic-1000mg-mvpcare-sin-sabor/p/MLM61391226#polycard_client=recommendations_pdp-v2p&reco_backend=recomm-platform_rars-vpp-v2p-supermarket-repurchase_supermarket&reco_model=fallback_organicos_deduplication&reco_client=pdp-v2p&reco_item_pos=2&reco_backend_type=low_level&reco_id=337a84f6-2a9b-4761-8a4d-506e29792855&wid=MLM2844751925&sid=recos