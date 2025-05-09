import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
import csv
from pathlib import Path
import time


class ConsultSeleniumSpider(scrapy.Spider):
    name = "consult_selenium"
    allowed_domains = ["consult.cbso.nbb.be"]

    def start_requests(self):
        csv_path = Path(__file__).parents[2] / "test_entreprise.csv"
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                raw_num = row.get("EnterpriseNumber", "").strip()
                numero = raw_num.replace(".", "")
                if numero:
                    url = f"https://consult.cbso.nbb.be/consult-enterprise/{numero}"
                    yield scrapy.Request(url=url, callback=self.parse, meta={"numero": numero})

    def parse(self, response):
        numero = response.meta["numero"]

        # Configuration Selenium (headless)
        options = Options()
        options.add_argument("--headless=new")
        driver_path = "C:/Drivers/chromedriver-win64/chromedriver.exe"
        driver = webdriver.Chrome(service=Service(driver_path))

        # Chargement de la page
        driver.get(response.url)

        try:
            # Attente que les blocs soient chargés
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "app-deposit-item"))
            )
            time.sleep(2)  # Laisse Angular charger

            # Extraction du HTML rendu
            sel = Selector(text=driver.page_source)

            documents = []
            for deposit in sel.css("app-deposit-item"):
                model = deposit.css("div.tile__title h3::text").get()
                statut = deposit.css("div.under-title::text").get()
                ref = deposit.css("span#userDepositId::text").get()
                date_depot = deposit.css("span#userDepositStartDate::text").get()
                date_exercice = deposit.css("div#userDepositEndDate::text").get()
                langue = deposit.css("span#userDepositLanguage::text").get()
                pdf_link = deposit.css("div.tile__actions a::attr(href)").get()
                if pdf_link:
                    pdf_link = response.urljoin(pdf_link)

                documents.append({
                    "model": model.strip() if model else None,
                    "statut": statut.strip() if statut else None,
                    "reference": ref.strip() if ref else None,
                    "date_depot": date_depot.strip() if date_depot else None,
                    "date_exercice": date_exercice.strip() if date_exercice else None,
                    "langue": langue.strip() if langue else None,
                    "lien_pdf": pdf_link
                })

            yield {
                "numero": numero,
                "documents": documents
            }

        finally:
            driver.quit()
