import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["entreprises_db"]

kbo = db["kbo_spider"]
ejustice = db["ejustice"]
consult = db["consult_selenium"]
fusion = db["entreprises_completes"]

fusion.drop()  # pour un nouveau départ

numeros = kbo.distinct("numero")
for numero in numeros:
    entreprise = kbo.find_one({"numero": numero}) or {}
    justice = ejustice.find_one({"numero": numero}) or {}
    bnb = consult.find_one({"numero": numero}) or {}

    fusion.insert_one({
        "numero": numero,
        "url": entreprise.get("url"),
        "generalites": entreprise.get("generalites"),
        "fonctions": entreprise.get("fonctions"),
        "capacites_entrepreneuriales": entreprise.get("capacites_entrepreneuriales"),
        "qualites": entreprise.get("qualites"),
        "autorisations": entreprise.get("autorisations"),
        "codes_nace": entreprise.get("codes_nace"),
        "donnees_financieres": entreprise.get("donnees_financieres"),
        "liens_entites": entreprise.get("liens_entites"),
        "liens_externes": entreprise.get("liens_externes"),
        "publications_ejustice": justice.get("publications", []),
        "documents_consult": bnb.get("documents", [])
    })

print(f"✅ Fusion terminée : {fusion.count_documents({})} entreprises insérées.")
