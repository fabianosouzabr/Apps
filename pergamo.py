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

@app.get('/redirect')
def redirect():
    return '''
    <html>
    <a href='http://localhost:4567/authorize'>Clique aqui para autenticar</a>
    </html>
    '''

@app.get('/login')
def login():
    return "<a href='" + meli.auth_url(redirect_URI=REDIRECT_URI) + "'>Clique aqui para Login</a>"

@app.get('/authorize')
def authorize():
    if request.query.get('code'):
        meli.authorize(request.query.get('code'), REDIRECT_URI)
    return "<a href='http://localhost:4567/index'>Ir ao índice</a>"
#    return meli.access_token

@app.get('/index')
def index():
    return '''
    <html>
    <p><a href='http://localhost:4567/user'>Informações do Usuário\n</a></p>
    <p><a href='http://localhost:4567/items'>Produtos\n</a></p>
    <p><a href='http://localhost:4567/user'>Pedidos\n</a></p>
    <p><a href='http://localhost:4567/user'>Perguntas\n</a></p>
    <p><a href='http://localhost:4567/user'>Pagamentos\n</a></p>
    <p><a href='http://localhost:4567/user'>Envios\n</a></p>
    <p></p>
    <p><a href='http://localhost:4567/index'>Ir ao índice</a></p>
    </html>
    '''

@app.get('/user')
def user():
    response = meli.get("users/256943677")
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