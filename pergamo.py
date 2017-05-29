#!python
import os
import json
import sys
from bottle import template

LIB_PATH = os.path.join('.', 'python3-sdk', 'lib')
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

userdata = None


@app.get('/')
@app.get('/login')
def login():
    return "<a href='" + meli.auth_url(redirect_URI=REDIRECT_URI) + "'>Clique aqui para Login</a>"


@app.get('/redirect')
@app.get('/authorize')
def authorize():
    if request.query.get('code'):
        meli.authorize(request.query.get('code'), REDIRECT_URI)
    return "<a href='http://localhost:4567/index'>Usuário Autorizado. Ir ao índice</a>"


@app.get('/index')
def index():
    global userdata
    params = {'access_token': meli.access_token}
    response = meli.get("/users/me", params=params)
    userdata = response.json()
    return '''
    <html>
    <h1><p>Menu Principal</p></h1>
    <h2><p>''' + str(userdata['nickname']) + '''</p></h2>
    <p><a href='http://localhost:4567/user'>Informações do Usuário</a></p>
    <p><a href='http://localhost:4567/items'>Anúncios</a></p>
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
    global userdata
    return '''
    <html>
    <h1><p>Dados do Usuário</p></h1>
    <p><div> ''' + str(userdata) + ''' </div></p>
    <p></p>
    <p><a href='http://localhost:4567/index'>voltar ao índice</a></p>
    </html>   
    '''


@app.get('/items')
def items():
    global userdata
    params = {'access_token': meli.access_token}
    response = meli.get("/users/" + str(userdata['id']) + "/items/search", params=params)
    items_list = response.json()
    return '''
    <html>
    <h1><p>Itens Anunciados</p></h1>
    ''' + template('simple.tpl', items_list) + '''
    <p><a href='http://localhost:4567/index'>voltar ao índice</a></p>
    </html>   
    '''


@app.get('/item/<item_id>')
def item_data(item_id):
    response = (meli.get("/items/" + item_id))
    jresponse = response.json()
    print("Item Details: " + str(jresponse))
    item_details = product_to_html(jresponse)

    response = (meli.get("/items/" + item_id + "/variations"))
    jresponse = response.json()
    print("Item Variations: " + str(jresponse))
    variations = dict_to_html(jresponse)

    return '''
    <html>
        <head>
        <style>
        div {
            text-align: justify;
            text-justify: inter-word;
            }
        </style>
        </head>
        <body>
            <h1><p>Dados do item</p></h1>
            <p><a href='http://localhost:4567/items'>voltar à lista de anúncios</a></p>
            <p><div><h2>Detalhes</h2>''' + item_details + ''' </div></p>
            <p><div><h2>Variações</h2>''' + variations + ''' </div></p>
            <p><a href='http://localhost:4567/items'>voltar à lista de anúncios</a></p>
        </body>
    </html>   
    '''


def product_to_html(dd):
    """Generate an HTML list of the keys and
    values in the dictionary dd, return a
    string containing HTML"""

    category_id = dd['category_id']
    print("Category ID: ")
    print (category_id)
    response = (meli.get("/categories/" + category_id))
    category_details = response.json()
    print ("Category Details: ")
    print (type(category_details))
    print (category_details)

    response = (meli.get("/categories/" + category_id +"/attributes"))
    cat_attrib = json.loads(response.text)
    category_attributes = {item['id']: item for item in cat_attrib}
    print ("Category Attributes: ")
    print (category_attributes)

    html = ""
    category_path = category_details['path_from_root']
    for i in range(len(category_path)):
        cat = category_path[i]
        html += '''<strong>> %s </strong>''' % (cat['name'])
    html += "<ol>"
    htmla = ""
    for key in dd:
        if key in ['id', 'title', 'category_id']:
            html += "<li><strong>%s: </strong>%s</li>" % (key, dd[key])
        if key in ['attributes']:
            htmla = "<h3>Atributos</h3>"
            htmla += '''<style type="text/css">
                            .fieldset-auto-width 
                            {display: inline-block;}
                            </style>'''
            attr_list = dd[key]
            for attr in attr_list:
                htmla += '''<form><div><fieldset class="fieldset-auto-width"><legend>%s (%s)</legend>''' % (attr['id'],attr['name'])
                #htmla += "--------Grupo de Atributos: %s (%s)</legend>" % (attr['attribute_group_id'], attr['attribute_group_name'])
                #htmla += '''<div><strong>%s: </strong><input type="text" name =%s value=%s></div>''' % ('value_id', 'value_id', attr['value_id'])
                if 'values' in category_attributes[attr['id']]:
                    htmla += '''%s ''' % (attr['value_name'])
                    htmla += '''<select name="%s">''' % ('value_name')
                    for n in category_attributes[attr['id']]['values']:
                        htmla += '''<option value="%s">%s</option>''' % (n['name'],n['name'])
                    htmla += '''</select>'''
                else:
                    htmla += '''<strong>%s: </strong><input type="text" name =%s value=%s>''' % ('value_name', 'value_name', attr['value_name'])
                htmla += '''<input type="submit" value="Alterar"></fieldset></div></form>'''
            htmla += "</ol>"
    html += "</ol>"
    html += htmla
    return html


def dict_to_html(dd):
    """Generate an HTML list of the keys and
    values in the dictionary dd, return a
    string containing HTML"""

    html = "<ol>"
    for key in dd:
        html += "<li><strong>%s: </strong>%s</li>" % (key, dd[key])
    html += "</ol>"
    return html


@app.get('/item/<item_id>/add_attributes')
def add_attributes(item_id):
    return '''
    <html>
        <head>
        <style>
        div {
            text-align: justify;
            text-justify: inter-word;
            }
        </style>
        </head>
        <body>
            <h1><p>Dados do item</p></h1>
            <p><a href='http://localhost:4567/items'>voltar à lista de anúncios</a></p>
            <p><div><h2>Detalhes</h2>''' + item_details + ''' </div></p>
            <p><div><h2>Variações</h2>''' + variations + ''' </div></p>
            <p><a href='http://localhost:4567/items'>voltar à lista de anúncios</a></p>
        </body>
    </html>   
    '''


@app.error(404)
def error404(error):
    return 'Erro 404. Parece que não há nada aqui!'


run(app, host='localhost', port=4567, reloader=True)

print(CLIENT_NAME)
