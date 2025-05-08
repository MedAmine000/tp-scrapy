import json

# Charger le fichier JSON
with open("c:\\M1_IPSSI_Korniti\\Cours\\WEB_Scrap\\Scrapy\\entreprises_scraper\\test_ejustice.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Trouver le numéro et compter les publications
numero = "0200068636"
for item in data:
    if item["numero"] == numero:
        taille_publications = len(item["publications"])
        print(f"Le numéro {numero} a {taille_publications} publications.")
        break