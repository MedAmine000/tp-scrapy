import scrapy
import csv
from pathlib import Path

class KboSpider(scrapy.Spider):
    name = "kbo_spider"
    allowed_domains = ["kbopub.economie.fgov.be"]

    def start_requests(self):
        csv_path = Path(__file__).parents[2] / "test_entreprise.csv"
        self.logger.info(f"Lecture du fichier CSV : {csv_path}")

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                raw_num = row.get("EnterpriseNumber", "").strip()
                numero = raw_num.replace(".", "")  # Supprime les points
                if numero.isdigit():
                    url = f"https://kbopub.economie.fgov.be/kbopub/toonondernemingps.html?lang=fr&ondernemingsnummer={numero}"

                    self.logger.info(f"URL générée : {url}")
                    yield scrapy.Request(
                        url,
                        callback=self.parse,
                        headers={
                            "Accept-Language": "fr",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                                        "Chrome/123.0.0.0 Safari/537.36"
                        }
                    )
    def extract_generalites(self, response):
        rows = response.xpath('//div[@id="table"]//tr')
        generalites = {}
        in_section = False

        for row in rows:
            section_title = row.xpath('.//h2/text()').get()
            if section_title:
                if "Généralités" in section_title:
                    in_section = True
                    continue
                elif in_section:
                    break  # on quitte la section une fois un nouveau <h2> trouvé

            if in_section:
                key = row.xpath('.//td[1]/text()').get()
                value = row.xpath('.//td[2]//text()').get()
                if key and value:
                    generalites[key.strip().rstrip(":")] = value.strip()

        return generalites

    def extract_qualites(self, response):
        rows = response.xpath('//div[@id="table"]//tr')
        qualites = []
        in_section = False

        for row in rows:
            section_title = row.xpath('.//h2/text()').get()
            if section_title:
                if "Qualités" in section_title:
                    in_section = True
                    continue
                elif in_section:
                    break  # fin de section

            if in_section:
                cell = row.xpath('.//td[@class="QL"]')
                if cell:
                    textes = cell.xpath('.//text()').getall()
                    qualite = " ".join(t.strip() for t in textes if t.strip())
                    if qualite:
                        qualites.append(qualite)

        return qualites

    def extract_autorisations(self, response):
        rows = response.xpath('//div[@id="table"]//tr')
        autorisations = []
        in_section = False

        for row in rows:
            section_title = row.xpath('.//h2/text()').get()
            if section_title:
                if "Autorisations" in section_title:
                    in_section = True
                    continue
                elif in_section:
                    break  # on sort dès qu'une autre section commence

            if in_section:
                liens = row.xpath('.//td[@class="QL"]//a')
                for lien in liens:
                    url = lien.xpath('./@href').get()
                    label = lien.xpath('normalize-space(string())').get()
                    if url and label:
                        autorisations.append({
                            "label": label.strip(),
                            "url": response.urljoin(url)
                        })

        return autorisations

    def extract_codes_nace(self, response):
        rows = response.xpath('//div[@id="table"]//tr')

        nace_2025 = []
        nace_2008 = []
        nace_2003 = []
        section = None

        for row in rows:
            section_title = row.xpath('.//h2/text()').get()
            if section_title:
                if "2025" in section_title:
                    section = "2025"
                    continue
                elif "2008" in section_title:
                    section = "2008"
                    continue
                elif "2003" in section_title:
                    section = "2003"
                    continue
                else:
                    section = None

            if section:
                cell = row.xpath('.//td[@class="QL"]')
                if not cell:
                    continue
                raw_texts = cell.xpath('.//text()').getall()
                texte = " ".join(t.strip() for t in raw_texts if t.strip())
                code = cell.xpath('.//a/text()').get()
                url = cell.xpath('.//a/@href').get()

                bloc = {
                    "texte": texte,
                    "code": code,
                    "url": response.urljoin(url) if url else None
                }

                if section == "2025":
                    nace_2025.append(bloc)
                elif section == "2008":
                    nace_2008.append(bloc)
                elif section == "2003":
                    nace_2003.append(bloc)

        return {
            "2025": nace_2025,
            "2008": nace_2008,
            "2003": nace_2003
        }
    def extract_donnees_financieres(self, response):
        rows = response.xpath('//div[@id="table"]//tr')
        donnees = {}
        in_section = False

        for row in rows:
            section_title = row.xpath('.//h2/text()').get()
            if section_title:
                if "Données financières" in section_title:
                    in_section = True
                    continue
                elif in_section:
                    break

            if in_section:
                key = row.xpath('.//td[1]/text()').get()
                value = row.xpath('.//td[2]//text()').get()
                if key and value:
                    donnees[key.strip().rstrip(":")] = value.strip()

        return donnees

    def extract_liens_entites(self, response):
        rows = response.xpath('//div[@id="table"]//tr')
        liens = []
        in_section = False

        for row in rows:
            section_title = row.xpath('.//h2/text()').get()
            if section_title:
                if "Liens entre entités" in section_title:
                    in_section = True
                    continue
                elif in_section:
                    break

            if in_section:
                bloc = row.xpath('.//td[@class="QL"]')
                if bloc:
                    url = bloc.xpath('.//a/@href').get()
                    texte = " ".join(bloc.xpath('.//text()').getall()).strip()
                    if texte:
                        liens.append({
                            "texte": texte,
                            "url": response.urljoin(url) if url else None
                        })

        return liens

    def extract_liens_externes(self, response):
        rows = response.xpath('//div[@id="table"]//tr')
        liens = []
        in_section = False

        for row in rows:
            section_title = row.xpath('.//h2/text()').get()
            if section_title:
                if "Liens externes" in section_title:
                    in_section = True
                    continue
                elif in_section:
                    break

            if in_section:
                anchors = row.xpath('.//a')
                for a in anchors:
                    url = a.xpath('./@href').get()
                    texte = a.xpath('normalize-space(string())').get()
                    if texte and url:
                        liens.append({
                            "texte": texte,
                            "url": url
                        })

        return liens

    def extract_fonctions(self, response):
        rows = response.xpath('//div[@id="table"]//tr')
        fonctions = []
        in_section = False

        for row in rows:
            section_title = row.xpath('.//h2/text()').get()
            if section_title:
                if "Fonctions" in section_title:
                    in_section = True
                    continue
                elif in_section:
                    break  # fin de section

            if in_section:
                # On cherche les lignes du tableau contenant les 3 colonnes
                cols = row.xpath('.//td[@class="RL"]')
                if len(cols) >= 3:
                    fonction = cols[0].xpath("normalize-space(string())").get()
                    nom = cols[1].xpath("normalize-space(string())").get()
                    date = cols[2].xpath("normalize-space(string())").get()

                    fonctions.append({
                        "fonction": fonction,
                        "nom": nom,
                        "date": date
                    })

        return fonctions

    def extract_capacites(self, response):
        rows = response.xpath('//div[@id="table"]//tr')
        capacites = []
        in_section = False

        for row in rows:
            section_title = row.xpath('.//h2/text()').get()
            if section_title and "Capacités entrepreneuriales" in section_title:
                in_section = True
                continue
            elif in_section and row.xpath('.//h2'):
                break

            if in_section:
                text = " ".join(row.xpath('.//text()').getall()).strip()
                if text:
                    capacites.append(text)

        return capacites


    def parse(self, response):
        numero = response.url.split("=")[-1]

        data = {
            "numero": numero,
            "url": response.url,
            "generalites": self.extract_generalites(response),
            "fonctions": self.extract_fonctions(response),
            "capacites_entrepreneuriales": self.extract_capacites(response),  # si existante
            "qualites": self.extract_qualites(response),
            "autorisations": self.extract_autorisations(response),
            "codes_nace": self.extract_codes_nace(response),
            "donnees_financieres": self.extract_donnees_financieres(response),
            "liens_entites": self.extract_liens_entites(response),
            "liens_externes": self.extract_liens_externes(response),
        }

        yield data

