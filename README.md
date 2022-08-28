## Web Scrapin + ETL + Analise de Dados

> *Script voltado para realizar a "raspagem" de dados na web (web scraping), com esses dados brutos em mãos irei aplicar algumas técnicas simples de transformação de dados (ETL), para que posteriormente essas dados possam ser analisados em alguma ferramenta de BI, neste caso será em Ecxel.*

* ### *Informações*
1. * **Linguagem de Programação Utilizada**
>Python 3.10.6

2. * **Bibliotecas**
>1. selenium 
>2. BeautifulSoup
>3. requests
>4. Pandas

------------

* ### Mapa do código

1. *Inicio o programa, declarando 2 arrays, o array de nome `elements_html` irá armazenar todos os elemetos html que irei precisar acessar, e o array de nome `array_prod` irá armazenar os valores que estão dentro dos elementos html, depois transformarei esse array em um Dataframe*

~~~python

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

~~~

-------

2. *Inicio a instancia com com o navegador e como argumento informo que a execução será em modo headless/invisivel, ou sejá o navegador será executado em memória apenas, ficando transparente para o usuário, aqui é usado a biblioteca selenium, repare que estamos apenas criando a intancia e argumentando, não executamos o navegador ainda.*

~~~python

options = webdriver.ChromeOptions()
options.add_argument("--headless")

~~~
----

3. *Neste bloco varias coisas acontecem, todas elas na biblioteca selinium, na primeira linha ocorre uma entrada de dados é onde o usuário informa qual produto deseja extrair os dados, na segunda linha, passamos para a variavel `url` o caminho para o site com o produto que iremos filtrar, na terceira linha jogados a instancia do navegador já pronto para execução na variavel `browser`, na quarta linha de fato executamos o navegador passando como parametro a variavel `url` no método `get`*
>**Todo esse processo no `selenium` foi necessário apenas para carregar o html que é executado por um Ajax em tempo de execução, sem isso não seria possivel pegar todos os elementos da pagina**

~~~python
name_prod = input('Informe o nome do produto:').replace(' ','-')

url = f'https://lista.mercadolivre.com.br/{name_prod}'

browser = webdriver.Chrome(executable_path=r'C:\Users\T-Gamer\Downloads\chromedriver_win32\chromedriver.exe',
                           chrome_options=options)
browser.get(url)
~~~
-----------

4. *Aqui iremos começar a utilizar as bibliotecas `requests` e `BeautifulSoup`, na primeira linha informamos que somos um navegador seguro, na segunda linha executamos o metodo `get` da biblioteca `requests` na pagina que foi carregada pelo `selenium`, na terceira linha pegamos todo o documento html e fazemos um parser utilizando o `lxml` que é muito performatico em comparação aos outros tipo de parser*

~~~python
header = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}
site = requests.get(url, headers=header)
soup = BeautifulSoup(site.content, 'lxml')
~~~
-----

5. *Este tricho é apenas para pegar a informação da ultima pagina da listagem de produtos, pois iremos iterar sobre todas as paginas* 

~~~python
int_last_page = soup.find('li', class_=elements_html[4]).get_text().strip()
idx = int_last_page.find(' ')
last_page = int_last_page[idx:]
~~~
----------

6. *Iremos fazer um ´for´ aninhado, o primeiro for é para iterar sobre todas as paginas daquele produto que estamos buscando, o sefundo ´for´ ira iterar sobre todos os produtos dentro de uma pagina para retornar nome,preço, descição e link, realizamos um append no nosso dicionario ´array_prod´ a cada iteração do ´for´ de produtos*

~~~python
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
~~~

----------

7. *Aqui iremos começar a utilizar a biblioteca pandas, na primeira linha transformo o nosso dicionario array_prod em um DataFrame, dessa forma podemos exportar para um arquivo de analise de dados, na segunda linha pego esse dataframe e retiro as linhas duplicadas, me baseio na coluna nome, depois de retirar todos os nomes duplicados eu irei exportar este dataframe para o excel e assim podemos realizar a analise dos dados coletados*

~~~python
df = pd.DataFrame(array_prod)
df.drop_duplicates(subset='Descricao').to_excel(r'C:\Users\T-Gamer\Downloads\analise_mercado_livre.xlsx',
            sheet_name=name_prod,encoding='utf-8-sig',index=False ,header=True)
~~~

-------------

## *O resultado será este*

* **Executando o programa, terminal adcionando os valores recuperados e já transformados no nosso dicionario `array_prod`**

<img src = img/img_1.png>

* **Resultado final com os dados já prontos para serem analisados em excel**

<img src = img/img_2.png>
