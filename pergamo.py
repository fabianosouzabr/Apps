#!python
import sys

sys.path.append('C:\\Users\\fmsouza\\PycharmProjects\\Apps\\python-sdk\\lib')
from meli import Meli
from bottle import Bottle, run, template, route, request

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
    <a href='http://localhost:4567/user'>Informações do Usuário</a>
    <a href='http://localhost:4567/user'>Produtos</a>
    <a href='http://localhost:4567/user'>Pedidos</a>
    <a href='http://localhost:4567/user'>Perguntas</a>
    <a href='http://localhost:4567/user'>Pagamentos</a>
    <a href='http://localhost:4567/user'>Envios</a>
    </html>
    '''

@app.get('/user')
def user():
    response = meli.get("/items/ITEM_ID")
    return '''
    <html>
    <div> ''' + str(response) + ''' </div>
    <a href='http://localhost:4567/index'>voltar ao índice</a>
    </html>   
    '''


@app.error(404)
def error404(error):
    return 'Erro 404. Parece que não há nada aqui!'

run(app, host='localhost', port=4567, reloader=True)



print(CLIENT_NAME)