import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup


# leitura das urls API
def pega_URLs_Nomes_salva_arquivo():
    url: str = 'https://cursos.alura.com.br/api/categorias'
    df_json: pd.DataFrame = pd.read_json(url, orient='records')

    inicio: str = 'https://cursos.alura.com.br/forum/subcategoria-'
    fim: str = '/sem-resposta/1'
    
    lista_link_nome = [((inicio + subcategoria['slug'] + fim), subcategoria['nome']) for categoria in df_json['subcategorias'] for subcategoria in categoria]
    
    df: pd.DataFrame = pd.DataFrame(lista_link_nome,columns=["URL", 'Nome'])
    df.to_csv('urls_subcategorias.csv', index=False)

#calculo da quantidade de duvidas
def pega_qtd_topicos_salva_arquivo():

    df = pd.read_csv('urls_subcategorias.csv')

    lista = []
    qtd_topicos = 20

    for url in df['URL']:

        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')        
        qtd_pag = len(soup.find_all(class_='paginationLink'))
        
        page = requests.get(url[:-1] + str(qtd_pag))    
        soup = BeautifulSoup(page.text, 'html.parser')        
        qtd_topicos_ultima_pag =  len(soup.find_all(class_='forumList-item-subject'))
        
        total_sub = qtd_topicos_ultima_pag + ((qtd_pag - 1) * qtd_topicos) if qtd_pag > 1 else qtd_topicos_ultima_pag    
        lista.append(total_sub)

    df['Quantidade'] = lista
    df.to_csv('subcategoria_topicos_sem_resposta.csv', index=False)

if __name__ == '__main__':
    start_time = datetime.now()
    pega_qtd_topicos_salva_arquivo()
    end_time = datetime.now()
    print('Duração: {}'.format(end_time - start_time))
