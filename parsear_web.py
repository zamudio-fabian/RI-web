# -*- coding: utf-8 -*-

import sys
import urllib2
from urlparse import urljoin
from bs4 import BeautifulSoup


def obtener_enlaces(url):
    print "ANALIZANDO: " + str(url)
    try:
        r = urllib2.urlopen(url)
        soup = BeautifulSoup(r, "lxml")
        tags_a = soup.find_all("a", href=True)
        return [tag_a["href"] for tag_a in tags_a]
    except urllib2.HTTPError, urllib2.URLError:
        return []


def main(url):
    lista_enlaces = obtener_enlaces(url)
    print "\nLista de enlaces encontrados:"
    for enlace in lista_enlaces:
        enlace = urljoin(url, enlace)
        print enlace

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print u"ERROR: Debe pasar como parámetro la url a consultar."
    else:
        main(sys.argv[1])
