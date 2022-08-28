from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import  pandas as pd


elements_html = \
    [
        'price-tag-fraction', #Preço
        'ui-search-item__title', #Descricao
        'ui-search-official-store-label ui-search-item__group__element ui-search-color--GRAY', #Vendido Por
        'ui-search-link', #Link
        'andes-pagination__page-count' #Ultima pagina
    ]

array_prod = \
    {
        'Preco'         :[],
        'Descricao'     :[],
        'Vendido Por'   :[],
        'Link'          :[]
     }

options = webdriver.ChromeOptions()
options.add_argument("--headless")

name_prod = input('Informe o nome do produto:').replace(' ','-')

url = f'https://lista.mercadolivre.com.br/{name_prod}'

browser = webdriver.Chrome(executable_path=r'C:\Users\T-Gamer\Downloads\chromedriver_win32\chromedriver.exe',
                           chrome_options=options)
browser.get(url)

header = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}
site = requests.get(url, headers=header)
soup = BeautifulSoup(site.content, 'lxml')

int_last_page = soup.find('li', class_=elements_html[4]).get_text().strip()
idx = int_last_page.find(' ')
last_page = int_last_page[idx:]

for j in range(1, int(last_page)+1):
    pages = f'https://lista.mercadolivre.com.br/{name_prod}_Desde_{j}_NoIndex_True'
    site = requests.get(pages, headers=header)
    soup = BeautifulSoup(site.content, 'html.parser')
    products = soup.findAll('div',class_='ui-search-result__content-wrapper')

    for product in products:

        name = product.find('h2', class_=elements_html[1]).get_text().strip()
        price = product.find('span', class_=elements_html[0]).get_text().strip().replace('.', '')
        link = product.find('a', class_=elements_html[3]).get('href')

        if product.find('p', class_=elements_html[2]) != None:
            elemt = product.find('p', class_=elements_html[2]).get_text().strip()
            p_treatment = elemt.find('por ')
            provider = elemt[p_treatment:].replace('por', '').lstrip()

        array_prod['Preco'].append(price)
        array_prod['Descricao'].append(name)
        array_prod['Vendido Por'].append(provider)
        array_prod['Link'].append(link)

        print(name, price,provider)

df = pd.DataFrame(array_prod)
df.drop_duplicates(subset='Descricao').to_excel(r'C:\Users\T-Gamer\Downloads\analise_mercado_livre.xlsx',
            sheet_name=name_prod,encoding='utf-8-sig',index=False ,header=True)

browser.close()

