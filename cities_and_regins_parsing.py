import pandas as pd
import requests
import lxml
from bs4 import BeautifulSoup
import xml
import time
import random
from fake_useragent import UserAgent

class Parser:
    def __init__(self):
        self.url = 'https://moi-goroda.ru/sitemap.xml'
        self.data = []
        self.ind = 0
        self.ua = UserAgent()


    def collect_all_pages(self):

        response = requests.get(url=self.url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'xml')

        urls = soup.find_all("loc")
        region_urls = [url.text for url in urls if url.text.startswith("https://moi-goroda.ru/region/") and 'all' not in url.text and 'list' in url.text]

        return region_urls


    def parsing_cities(self):

        region_urls = self.collect_all_pages()


        for url in region_urls:
            try:
                headers = {
                    'User-Agent': self.ua.random,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8',
                    'Connection': 'keep-alive'
                }

                response = requests.get(url=url, headers=headers, timeout=30)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'lxml')

                try:
                    region = soup.select_one('#page-header').text.strip()
                except:
                    region = ''

                try:
                    cities = [u.text.strip().capitalize() for u in soup.select_one('#list-content').select('.d-flex.align-items-center.justify-content-center')]
                except:
                    cities = []

                for city in cities:
                    self.data.append({
                        'Регион': region,
                        'Город': city,
                    })

                # Случайная задержка между запросами
                time.sleep(random.uniform(1, 2))

            except Exception as e:
                print(f"Ошибка при обработке {url}: {e}")
                continue





parser = Parser()
parser.parsing_cities()

df = pd.DataFrame(parser.data)
df.to_excel('region.xlsx', index=False)