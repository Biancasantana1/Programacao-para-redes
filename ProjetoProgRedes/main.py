import requests
import json

def save_csv(data, titulo):
    arquivo = open(titulo + '.csv', 'w')
    arquivo.write(data)
    arquivo.close()


url = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes'
#anos = [2018, 2019, 2020, 2021, 2022, 2023]  # Adicione aqui os anos desejados
anos = list(range(2010, 2024))

itens_por_pagina = 100
siglas = ['PL', 'PEC', 'MPV', 'PDL', 'PLP', 'PFC', 'REQ', 'RIC', 'RCP', 'MSC']

autores_text = "nome;codTipo;Tipo;\n"
projetos_text = "id_proposicao;ano;tipo;numero;assunto;autores;cod_situacao;\n"

for ano in anos:
    params = {
        'siglaTipo': siglas,
        'ano': ano,
        'itens': itens_por_pagina,
        'pagina': 1
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        print(f'Requisição bem sucedida para o ano {ano}!')
    else:
        print(f'Erro na requisição para o ano {ano}.')

    data = json.loads(response.content)

    for prop in data['dados']:
        id_proposicao = prop['id']
        ano = prop['ano']
        tipo = prop['siglaTipo']
        numero = prop['numero']
        assunto = prop['ementa']

        url_tramitacoes = f'https://dadosabertos.camara.leg.br/api/v2/proposicoes/{id_proposicao}/tramitacoes'
        response_tramitacoes = requests.get(url_tramitacoes)
        data_tramitacoes = json.loads(response_tramitacoes.content)
        ultima_tramitacao = data_tramitacoes['dados'][-1]
        cod_situacao = ultima_tramitacao['codSituacao']
        desc_situacao = ultima_tramitacao['descricaoSituacao']

        urlAutores = f'https://dadosabertos.camara.leg.br/api/v2/proposicoes/{id_proposicao}/autores'
        responseAutores = requests.get(urlAutores)
        dataAutores = json.loads(responseAutores.content)

        autores = []
        for autor in dataAutores['dados']:
            nome = autor['nome']
            codTipo = autor['codTipo']
            tipoAutor = autor['tipo']
            autores_text += nome + ";" + str(codTipo) + ";" + tipoAutor + ";" + "\n"
            autores.append((nome, codTipo, tipoAutor))

        #print(id_proposicao, ano, tipo, numero, assunto, autores, cod_situacao)
        projetos_text += str(id_proposicao) + ";" + str(ano) + ";" + str(tipo) + ";" + str(
            numero) + ";" + assunto + ";" + str(autores) + ";" + str(cod_situacao) + ";\n"

#save_csv(autores_text, 'autores')
save_csv(projetos_text, 'projetos')
