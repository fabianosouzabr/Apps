import bs4
from bs4 import BeautifulSoup
arq=open('/home/fabiano/Documentos/Money/amex_junho.html','r')
tree=BeautifulSoup(arq.read())
tree('title')
for i in range(it):
        print (tree('table')[0]('td')[i].string)
