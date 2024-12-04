import re
import threading

import requests
from bs4 import BeautifulSoup

DOMINIO = "https://exemplo.com.br"
URL_AUTOMOVEIS = "https://exemplo.com.br/anuncios/"
LINKS = []
TELEFONES = []


# Requisição de Busca
def requisicao(url):
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta.text
        else:
            print("Erro ao fazer a requisição")
    except Exception as error:
        print("Erro ao fazer a requisição")
        print(error)


# Faz o PARSING
def parsing(resposta_html):
    try:
        soup = BeautifulSoup(resposta_html, 'html.parser')  # -> Faz o parsing # -> html.parser é o tipo de parsing
        return soup
    except Exception as error:
        print("Erro ao fazer parsing")
        print(error)


# Encontra os links do site
def encontrar_links(soup):
    try:
        # Filtra somente os links
        cards_pai = soup.find('div', class_='ui three doubling link cards')
        cards = cards_pai.find_all("a")
    except:
        print("Erro ao encontrar links")

    links = []
    for card in cards:
        try:
            link = card['href']
            links.append(link)
        except:
            pass

    return links


# Encontra o telefone
def encontrar_telefone(soup):
    # Filtra para encontrar somente a área da descrição do anuncio
    try:
        descricao = soup.find_all("div", class_="sixteen wide column")[2].p.get_text().strip()
    except Exception as error:
        print("Erro ao encontrar descrição")
        print(error)
        return None

    regex = re.findall(r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.\)]?\d{4})[ \-\.\)]?(\d{4})", descricao)
    # -> Função que acha todas as opções
    if regex:
        return regex


def descobrir_telefones():
    while True:
        try:
            link_anuncio = LINKS.pop(1)
        except:
            return None

        resposta_anuncio = requisicao(DOMINIO + link_anuncio)

        if resposta_anuncio:
            soup_anuncio = parsing(resposta_anuncio)
            if soup_anuncio:
                telefones = encontrar_telefone(soup_anuncio)
                if telefones:
                    for telefone in telefones:
                        print("Telefone encontrado: ", telefone)
                        TELEFONES.append(telefone)
                        salvar_telefones(telefone)


def salvar_telefones(telefone):
    string_telefone = "{}{}{}\n".format(telefone[0], telefone[1], telefone[2])
    try:
        with open("telefones.csv", "a") as arquivo:
            arquivo.write(string_telefone)
    except Exception as error:
        print("Erro ao salvar o arquivo!")
        print(error)


if __name__ == "__main__":
    resposta_busca = requisicao(URL_AUTOMOVEIS)
    if resposta_busca:
        soup_busca = parsing(resposta_busca)
        if soup_busca:
            LINKS = encontrar_links(soup_busca)

            THREADS = []
            for i in range(5):
                t = threading.Thread(target=descobrir_telefones)
                THREADS.append(t)

            for t in THREADS:
                t.start()

            for t in THREADS:
                t.join()
