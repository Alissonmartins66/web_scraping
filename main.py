import requests
from bs4 import BeautifulSoup
import re 
import pandas as pd 
import math
import os
from user_agent import user_agent

url = 'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer'

headers = {
    "User-Agent": user_agent #digite 'My user agent' em seu navegador e cole aqui.
    }

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
quant_itens = soup.find('div', id='listingCount').get_text(strip=True) 

quant_numbers = int(re.search(r'\d+', quant_itens).group())

last_page = math.ceil(int(quant_numbers)/ 20)

dic_products = {'brand':[], 'price': []}

for i in range(1, last_page +1):
    url_pag = f'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    all_products = soup.find_all('div', class_=re.compile('productCard'))

    for product in all_products:
        brand = product.find('span', class_=re.compile('nameCard')).get_text().strip()
        price = product.find('span', class_=re.compile('priceCard')).get_text().strip()

        dic_products['brand'].append(brand)
        dic_products['price'].append(price)

file_name = 'datakabum5.csv'

folder = r'C:/Users/.../.../Área de Trabalho/planilhaWeb' #insira um caminho para aonde queira salvar

File_path = os.path.join(folder, file_name)

df = pd.DataFrame(dic_products)
df.to_csv(File_path, index=False)

