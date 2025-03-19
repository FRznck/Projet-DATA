import requests
from bs4 import BeautifulSoup
import csv

base_url = "http://books.toscrape.com/catalogue/page-{}.html"

# Fonction pour extraire les données d'une page
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    page_data = []

    for book in books:
        # Titre
        title = book.h3.a["title"]

        # Prix
        price = book.find("p", class_="price_color").text.strip()

        # Catégorie (à extraire depuis la page du produit)
        product_link = "http://books.toscrape.com/catalogue/" + book.h3.a["href"]
        category = get_category(product_link)

        # Disponibilité
        availability = book.find("p", class_="instock availability").text.strip()

        # Note (étoiles)
        rating = book.find("p", class_="star-rating")["class"][1]  

        # Lien du produit
        product_link = "http://books.toscrape.com/catalogue/" + book.h3.a["href"]

        # Description (optionnel, à extraire depuis la page du produit)
        description = get_description(product_link)

        # Ajouter les données à la liste
        page_data.append({
            "titre": title,
            "prix": price,
            "categorie": category,
            "disponibilite": availability,
            "note": rating,
            "lien": product_link,
            "description": description
        })

    return page_data

# Fonction pour extraire la catégorie depuis la page du produit
def get_category(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, "html.parser")
    category = soup.find("ul", class_="breadcrumb").find_all("a")[2].text.strip()
    return category

# Fonction pour extraire la description depuis la page du produit
def get_description(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, "html.parser")
    description = soup.find("meta", attrs={"name": "description"})["content"].strip()
    return description

# Fonction principale pour scraper toutes les pages
def scrape_books_to_scrape():
    all_books_data = []
    for page in range(1, 51):  # Il y a 50 pages au total
        print(f"Scraping de la page {page}...")
        url = base_url.format(page)
        page_data = scrape_page(url)
        all_books_data.extend(page_data)

    return all_books_data

# Scraper les données
data = scrape_books_to_scrape()

# Sauvegarder les données dans un fichier CSV
with open("livres.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["titre", "prix", "categorie", "disponibilite", "note", "lien", "description"])
    writer.writeheader()
    writer.writerows(data)

print("Scraping terminé. Les données ont été sauvegardées dans 'livres.csv'.")