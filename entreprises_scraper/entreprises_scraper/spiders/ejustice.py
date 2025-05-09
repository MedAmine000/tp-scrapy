import scrapy
import csv
from pathlib import Path

class EjusticeSpider(scrapy.Spider):
    name = "ejustice"
    allowed_domains = ["ejustice.just.fgov.be"]

    def start_requests(self):
        csv_path = Path(__file__).parents[2] / "test_entreprise.csv"
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                raw_num = row.get("EnterpriseNumber", "").strip()
                numero = raw_num.replace(".", "")
                if numero:
                    url = f"https://www.ejustice.just.fgov.be/cgi_tsv/list.pl?btw={numero}"
                    yield scrapy.Request(
                        url,
                        callback=self.parse,
                        meta={"numero": numero}
                    )
    def parse(self, response):
        numero = response.meta["numero"]
        accumulated = response.meta.get("publications", [])

        # 1. Extraire publications de cette page
        for item in response.css("div.list-item"):
            content = item.css("div.list-item--content")
            denomination = content.css("p.list-item--subtitle font::text").get()
            titre_bloc = content.css("a.list-item--title::text").getall()
            titre_bloc = [t.strip() for t in titre_bloc if t.strip()]
            
            adresse = titre_bloc[0] if len(titre_bloc) > 0 else None
            num_entreprise = titre_bloc[1] if len(titre_bloc) > 1 else None
            type_publication = titre_bloc[2] if len(titre_bloc) > 2 else None
            date_reference = titre_bloc[3] if len(titre_bloc) > 3 else None

            image_url = content.css('a.standard::attr(href)').get()
            if image_url:
                image_url = response.urljoin(image_url)

            accumulated.append({
                "denomination": denomination,
                "adresse": adresse,
                "numero_entreprise": num_entreprise,
                "type": type_publication,
                "date_reference": date_reference,
                "image_url": image_url
            })

        # 2. Vérifier s'il existe une page suivante
        next_page = response.css('a.pagination-button.active + a::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse,
                meta={"numero": numero, "publications": accumulated}
            )
        else:
            # 3. Fin : yield l'objet complet
            yield {
                "numero": numero,
                "publications": accumulated
            }
    