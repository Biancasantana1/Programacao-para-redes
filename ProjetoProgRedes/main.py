import requests
import json

url = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes'
params = {
    'siglaTipo': 'PL',
    'ano': 2022,
    'itens': 100,
    'pagina': 1
}
response = requests.get(url, params=params)

if response.status_code == 200:
    print('Requisição bem sucedida!')
else:
    print('Erro na requisição.')

data = json.loads(response.content)
#print(data)

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
        autores.append((nome,codTipo, tipoAutor))

    print(id_proposicao, ano, tipo, numero, assunto, autores, cod_situacao)




