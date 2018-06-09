# -*- coding: utf-8 -*-

import sys
import urllib2
from urlparse import urljoin
from bs4 import BeautifulSoup
import graphviz as gv
import re
import ssl
import datetime


def crawlear_urls(lista_urls):
    id_url = 0
    largo_grafo = 50
    pendientes = []
    recorridas = []
    for url in lista_urls:
        pendientes.append({"id": id_url, "url": url, "out": []})
        id_url += 1
    while pendientes:
        enlaces = obtener_enlaces(pendientes[0]["url"])
        for enlace in enlaces:
            enlace = urljoin(pendientes[0]["url"], enlace)
            if enlace in recorridas:
                pendientes[0]["out"].append(recorridas[recorridas.index(enlace)]["id"])
            elif enlace in pendientes:
                pendientes[0]["out"].append(pendientes[pendientes.index(enlace)]["id"])
            else:
                pendientes.append({"id": id_url, "url": enlace, "out": []})
                pendientes[0]["out"].append(id_url)
                id_url += 1
        recorridas.append(pendientes[0])
        pendientes.pop(0)
        if len(recorridas) >= largo_grafo:
            break
    return recorridas


def obtener_enlaces(url):
    print "ANALIZANDO: " + str(url)
    try:
        r = urllib2.urlopen(url)
        soup = BeautifulSoup(r, "lxml")
        tags_a = soup.find_all("a", href=re.compile("http"))
        return [tag_a["href"] for tag_a in tags_a]
    except (urllib2.HTTPError, urllib2.URLError, ssl.CertificateError) as error:
        return []


def graficar_grafo(recorridas, nombre_grafo):
    grafo = gv.Digraph(format="svg")
    ids_obtenidos = {}
    for nodo in recorridas:
        nodo["url"] = nodo["url"].replace(":", "")  # El nombre del nodo no puede contener ":"
        grafo.node(nodo["url"])
        ids_obtenidos[nodo["id"]] = nodo["url"]
    for nodo in recorridas:
        for id_out in nodo["out"]:
            if id_out in ids_obtenidos:
                grafo.edge(str(nodo["url"]), str(ids_obtenidos[id_out]))
    grafo.render(nombre_grafo)


def main(urls, nombre_grafo):
    recorridas = crawlear_urls(urls)
    graficar_grafo(recorridas, nombre_grafo)
    print "Finalizado!"


if __name__ == "__main__":
    nombre = 'grafo_'+(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    if "-h" in sys.argv:
        print "MODO DE USO: python crawler.py URL_WITH_PROTOCOL"
        sys.exit(0)
    if len(sys.argv) < 2:
        print "ERROR: python crawler.py URL_WITH_PROTOCOL"
        sys.exit(1)
        
    main(sys.argv[1:], nombre)