#!python
import os
import sys
import pprint
import json

LIB_PATH = os.path.join('..','python3-sdk','lib')
print(LIB_PATH)
sys.path.append(LIB_PATH)
from meli import Meli

from bottle import Bottle, run, request

CLIENT_ID = '6383285056445610'
CLIENT_SECRET = 'Zya79p7R8hLkQaRfficgmEA8bNf30a7B'
REDIRECT_URI = '''http://localhost:4567/redirect'''
CLIENT_NAME = 'Stranger'

meli = Meli(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

app = Bottle()


@app.get('/login')
def login():
    return "<a href='" + meli.auth_url(redirect_URI=REDIRECT_URI) + "'>Clique aqui para Login</a>"

@app.get('/redirect')
@app.get('/authorize')
def authorize():
    if request.query.get('code'):
        meli.authorize(request.query.get('code'), REDIRECT_URI)
    return "<a href='http://localhost:4567/index'>Usuário Autorizado. Ir ao índice</a>"
#    return meli.access_token

@app.get('/index')
def index():
    return '''
    <html>
    <h1><p>Menu Principal</p></h1>
    <p><a href='http://localhost:4567/user'>Informações do Usuário</a></p>
    <p><a href='http://localhost:4567/items'>Produtos</a></p>
    <p><a href='http://localhost:4567/user'>Pedidos</a></p>
    <p><a href='http://localhost:4567/user'>Perguntas</a></p>
    <p><a href='http://localhost:4567/user'>Pagamentos</a></p>
    <p><a href='http://localhost:4567/user'>Envios</a></p>
    <p></p>
    <p><a href='http://localhost:4567/index'>Ir ao índice</a></p>
    </html>
    '''

@app.get('/user')
def user():
    params = {'access_token': meli.access_token}
    response = meli.get("/users/me", params=params)
    userdata = json.loads(response.text)
    print(userdata)
    return '''
    <html>
    <p><div> ''' + response.text + ''' </div></p>
    <p></p>
    <p><a href='http://localhost:4567/index'>voltar ao índice</a></p>
    </html>   
    '''

@app.get('/items')
def user():
    response = meli.get("items/MLB793080631")
    itemdata = json.loads(response.text)
    print(itemdata)
    return '''
    <html>
    <p><div> ''' + response.text + ''' </div></p>
    <p></p>
    <p><a href='http://localhost:4567/index'>voltar ao índice</a></p>
    </html>   
    '''

#793080631


@app.error(404)
def error404(error):
    return 'Erro 404. Parece que não há nada aqui!'

run(app, host='localhost', port=4567, reloader=True)



print(CLIENT_NAME)