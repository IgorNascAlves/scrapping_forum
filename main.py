# inicio do tempo
from datetime import datetime
start_time = datetime.now()


# leitura das urls API


import pandas as pd

url = 'https://cursos.alura.com.br/api/categorias'
df = pd.read_json(url, orient='records')

inicio = 'https://cursos.alura.com.br/forum/subcategoria-'
fim = '/sem-resposta/1'
lista_link_nome = [((inicio + subcategoria['slug'] + fim), subcategoria['nome']) for categoria in df['subcategorias'] for subcategoria in categoria]

df = pd.DataFrame(lista_link_nome)
df.to_csv('teste.csv', header=False, index=False)

# leitura das urls selenium

# from selenium import webdriver
# import pandas as pd

# driver = webdriver.Firefox()

# url_base = "https://cursos.alura.com.br/forum/todos/1"

# driver.get(url_base)

# categorias = driver.find_elements_by_class_name("dashboard-list-subcategory-link")

# categorias = [(categoria.get_attribute("href"),categoria.get_attribute("text").split()[0]) for categoria in categorias]

# driver.quit()

# df = pd.DataFrame(categorias)
# df.to_csv('teste.csv', header=False, index=False)

#calculo da quantidade de duvidas

df = pd.read_csv("teste.csv",names=["URL", 'nome'])
#df['url'] = [url[:-5] + 'sem-resposta/1' for url in df['URL']] #selenium

import re
import requests

lista = []
for url in df['URL']:
    sessao = requests.Session()
    resposta = sessao.get(url)
    regex = 'paginationLink'
    count = len(re.findall(regex, str(resposta.content)))

    resposta = sessao.get(url)
    regex = 'class="forumList-item-subject"'
    count_page = len(re.findall(regex, str(resposta.content)))

    resposta = sessao.get(url[:-1] + str(count))
    regex = 'class="forumList-item-subject"'
    count_last_pag = len(re.findall(regex, str(resposta.content)))

    total_sub = count_last_pag + ((count - 1) * count_page) if count else count_last_pag
    lista.append(total_sub)

df['count'] = lista

df.to_csv('teste2.csv', index=False)

#consulta

df = pd.read_csv("teste2.csv")
print(df.iloc[110][-2], df.iloc[110][-1], sep='\n')

#fim do tempo

end_time = datetime.now()
print('Duração: {}'.format(end_time - start_time))