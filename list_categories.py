import json
import pprint
#para verificar hash e data de criação do último dump de categorias:
#curl -I  https://api.mercadolibre.com/sites/MLB/categories/all
#Essa URL contém dois cabeçalhos que podem ser utilizados para verificar quando foi gerado o último dump.
#X-Content-Created: contém a data da última geração.
#X-Content-MD5: contém a soma de verificação MD5 da última geração.

#para buscar novo dump de categorias
#rodar na pasta raiz da aplicação:
#curl https://api.mercadolibre.com/sites/MLB/categories/all  > categoriesMLB.gz

cod_categoria = 'MLB70612'

try:
    arquivo_json = open('categoriesMLB','r')
    dados_json = json.load(arquivo_json)
    dados_categoria = dados_json[cod_categoria]
except Exception as erro:
    print("Ocorreu um erro ao carregar o arquivo.")
    print("O erro pe: {}".format(erro))

print(type(dados_categoria))
pprint.pprint(dados_categoria)

#curl https://api.mercadolibre.com/sites/MLB/search?category=MLB70612&condition=new&buying_mode=buy_it_now
