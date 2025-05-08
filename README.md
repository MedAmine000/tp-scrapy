# 📊 Scrapy - Collecte d'informations sur les entreprises belges

Ce projet Scrapy collecte, fusionne et stocke automatiquement des données publiques issues de trois sources officielles en Belgique :

- 🇧🇪 [KBO](https://kbopub.economie.fgov.be) – Banque-Carrefour des Entreprises
- 🧾 [eJustice](https://www.ejustice.just.fgov.be) – Publications au Moniteur belge
- 📂 [BNB Consult](https://consult.cbso.nbb.be) – Comptes annuels (Banque nationale de Belgique)

Toutes les données sont fusionnées dans une base MongoDB sous forme d’un document unique par entreprise.

---

## 🧰 Technologies

- **Scrapy** – Framework principal de web scraping
- **Selenium** – Pour scraper les pages dynamiques de `consult.cbso.nbb.be`
- **MongoDB** – Base de données NoSQL pour stocker les résultats
- **Python 3.10+**

---

## 🕷️ Spiders inclus

| Nom du spider      | Source                                 | Objectif principal                        |
|--------------------|----------------------------------------|--------------------------------------------|
| `kbo_spider`       | kbopub.economie.fgov.be                | Infos générales, fonctions, codes NACE     |
| `ejustice`         | ejustice.just.fgov.be                  | Publications légales au Moniteur belge     |
| `consult_selenium` | consult.cbso.nbb.be (avec Selenium)    | Comptes annuels et dépôts BNB              |

---

## 📦 Données extraites

### Depuis KBO :
- Généralités (statut, adresse, forme juridique…)
- Fonctions (administrateurs, mandataires…)
- Codes NACE (2003, 2008, 2025)
- Capacités entrepreneuriales
- Liens entre entités
- Données financières

### Depuis eJustice :
- Type de publication
- Date et référence
- Lien vers le PDF si disponible

### Depuis Consult BNB :
- Modèle de dépôt
- Référence, date de dépôt et fin d'exercice
- Langue et lien PDF du dépôt

---

## 🗃️ Structure MongoDB finale

Les données sont regroupées dans la collection `entreprises_completes` avec la structure suivante :

```json
{
  "numero": "0200068636",
  "url": "...",
  "generalites": { ... },
  "fonctions": [ ... ],
  "codes_nace": { ... },
  "capacites_entrepreneuriales": [ ... ],
  "donnees_financieres": { ... },
  "autorisations": [ ... ],
  "liens_entites": [ ... ],
  "liens_externes": [ ... ],
  "publications_ejustice": [ ... ],
  "documents_consult": [ ... ]
}
```

---

## 🔄 Processus de fusion

Une fois les spiders exécutés, un script Python `fusionner.py` combine toutes les données en un document unique par entreprise.

```bash
python fusionner.py
```

---

## 🏁 Lancer les spiders

```bash
scrapy crawl kbo_spider
scrapy crawl ejustice
scrapy crawl consult_selenium
```

---

## 📝 Auteurs

- 💻 Projet réalisé par Korniti MedAmine
- 🎓 Contexte : projet d'automatisation de la collecte de données pour des études économiques, juridiques ou statistiques sur les entreprises en Belgique

---

## ⚠️ Mentions

Les données sont extraites de sites publics pour des usages non commerciaux ou pédagogiques. Respectez les CGU des sites scrappés.
