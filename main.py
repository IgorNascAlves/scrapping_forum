import pandas as pd
import re
import requests


# leitura das urls API

url: str = 'https://cursos.alura.com.br/api/categorias'
df_json: pd.DataFrame = pd.read_json(url, orient='records')
inicio: str = 'https://cursos.alura.com.br/forum/subcategoria-'
fim: str = '/sem-resposta/1'
lista_link_nome = [((inicio + subcategoria['slug'] + fim), subcategoria['nome']) for categoria in df_json['subcategorias'] for subcategoria in categoria]
df: pd.DataFrame = pd.DataFrame(lista_link_nome,columns=["URL", 'Nome'])

#calculo da quantidade de duvidas

lista = []
sessao = requests.Session()
regex_paginas = 'paginationLink'
regex_topicos = 'class="forumList-item-subject"'

for url in df['URL']:

    resposta = sessao.get(url)
    resp_content_str = str(resposta.content)
    qtd_pag = len(re.findall(regex_paginas, resp_content_str))        
    qtd_topicos = len(re.findall(regex_topicos, resp_content_str))
    
    resposta = sessao.get(url[:-1] + str(qtd_pag))    
    qtd_topicos_ultima_pag = len(re.findall(regex_topicos, str(resposta.content)))    
    total_sub = qtd_topicos_ultima_pag + ((qtd_pag - 1) * qtd_topicos) if qtd_pag else qtd_topicos_ultima_pag    
    lista.append(total_sub)

df['Quantidade'] = lista
df.to_csv('subcategoria_topicos_sem_resposta.csv', index=False)
