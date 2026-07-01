from scraper.meli import scrape_product_meli
from db.connection import connect_database

#data = scrape_product_meli("https://www.mercadolibre.com.mx/panini-manga-mexico--berserk-13/up/MLMU587209408?matt_tool=28238160")
#print(data)

conn = connect_database()
print(conn)