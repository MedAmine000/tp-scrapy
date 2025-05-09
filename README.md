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




## Exemple de Document en sortie ...

```json
{
  "numero": "200068636",
  "url": "https://kbopub.economie.fgov.be/kbopub/toonondernemingps.html?ondernemingsnummer=200068636",
  "generalites": {
    "nom": "TUSSENGEMEENTELIJKE MAATSCHAPPIJ DER VLAANDEREN VOOR WATERVOORZIENING",
    "adresse": "STROPSTRAAT 1 9000 GENT"
  },
  "fonctions": [
    {
      "fonction": "Administrateur",
      "nom": "Foulon, Jan",
      "date": "Depuis le 22 juin 2007"
    }
  ],
  "capacites_entrepreneuriales": [
    "Pas de données reprises dans la BCE."
  ],
  "qualites": [
    "Employeur ONSS Depuis le 1 janvier 2022",
    "Pouvoir adjudicateur Depuis le 16 février 1923"
  ],
  "autorisations": [
    {
      "label": "BELAC - Laboratoire d'essais",
      "url": "https://weblist.economie.fgov.be/fr/belac/0200.068.636"
    }
  ],
  "codes_nace": {
    "2008": [
      {
        "texte": "TVA 2008 93.126 - Activités de clubs de sports nautiques Depuis le 22 juillet 2008",
        "code": "93.126",
        "url": null
      }
    ]
  },
  "donnees_financieres": {
    "Capital": "1.978.935,00 EUR",
    "Assemblée générale": "mai",
    "Date de fin de l'année comptable": "31 décembre"
  },
  "liens_entites": [
    {
      "texte": "0427.324.788 (AQUINTER) est absorbée par cette entité depuis le 23 décembre 2004",
      "url": "https://kbopub.economie.fgov.be/kbopub/toonondernemingps.html?ondernemingsnummer=427324788"
    }
  ],
  "liens_externes": [
    {
      "texte": "Publications au Moniteur belge",
      "url": "https://www.ejustice.just.fgov.be/cgi_tsv/list.pl?language=fr&btw=0200068636&page=1&view_numac=0200068636#SUM"
    }
  ],
  "publications_ejustice": [
    {
      "denomination": "FARYS",
      "adresse": "STROPSTRAAT 1 9000 GENT",
      "numero_entreprise": "200.068.636",
      "type": "STATUTEN (VERTALING, COÖRDINATIE, OVERIGE WIJZIGINGEN, …)",
      "date_reference": "2024-06-19",
      "url": "https://www.ejustice.just.fgov.be/tsv_pdf/2024/06/19/24092810.pdf"
    }
  ],
  "documents_consult": [
    {
      "model": "Model voor geconsolideerde jaarrekening",
      "statut": "Initial",
      "reference": "Référence 2024-00231588",
      "date_depot": "Date de dépôt 04/07/2024",
      "date_exercice": "31/12/2023",
      "langue": "NL",
      "lien_pdf": null
    }
  ]
}


## 📝 Auteurs

- 💻 Projet réalisé par Korniti MedAmine
- 🎓 Contexte : projet d'automatisation de la collecte de données pour des études économiques, juridiques ou statistiques sur les entreprises en Belgique

---

## ⚠️ Mentions

Les données sont extraites de sites publics pour des usages non commerciaux ou pédagogiques. Respectez les CGU des sites scrappés.
