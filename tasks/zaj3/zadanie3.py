# -*- coding: utf-8 -*-


################################################################################
### Kod pomocniczy od prowadzącego
################################################################################

import io
import bz2
import re
import csv
from xml.dom.pulldom import parse, START_ELEMENT

link_re = re.compile("\[\[([^\[\]\|]+)(?:\|[^\]]+)?\]\]")


def text_from_node(node):
    """
    Przyjmuje węzeł XML i zwraca kawałki zawartego w nim tekstu
    """
    for ch in node.childNodes:
        if ch.nodeType == node.TEXT_NODE:
            yield ch.data


def clean_page(page_contents):
    """
    Pobiera iterator tekstu i w (z dużymi błędami) usuwa z niego markup Wikipedii
    oraz normalizuje go.

    .. warning::

        Ten lgorytm czyszczenia markupu Wikipedii ma więcej wad niz zalet.
        W zasadzie zaletę ma jedną: nie wymaga instalacji parsera Wikipedii,
        i będzie tak samo działać na Windowsie co na Linuksie.

        Ogólnie jest tu duze pole do poprawy.
    """
    page = io.StringIO()
    for c in page_contents:
        page.write(c)

    page = page.getvalue()

    page = re.sub(r"[^a-zA-Z0-9\.\,\;\s]", " ", page, flags=re.UNICODE)
    page = re.sub("\s+", " ", page, flags=re.UNICODE | re.MULTILINE)

    return page


def iter_over_contents(IN):
    """
    Pobiera nazwę pliku i zwraca iterator który zwraca krotki
    (tytuł strony, wyczyszczona zawartość).

    Działa to na tyle sprytnie że nie ładuje całego XML do pamięci!
    :param IN:
    :return:
    """
    open_func = open
    if IN.endswith("bz2"):
        open_func = bz2.open
    with open_func(IN) as f:
        doc = parse(f)
        for event, node in doc:
            if event == START_ELEMENT and node.tagName == 'page':
                doc.expandNode(node)
                text = node.getElementsByTagName('text')[0]
                title = node.getElementsByTagName('title')[0]
                title = "".join(text_from_node(title))
                yield title, clean_page(text_from_node(text))

################################################################################
### Kod pomocniczy od prowadzącego === END
################################################################################


def generate_ngrams(contents, ngram_len=7):
    """
    Funkcja wylicza częstotliwość n-gramów w części wikipedii.
    N-gramy są posortowane względem zawartości n-grama.

    Testiowanie tej funkcji na pełnych danych może być uciążliwe, możecie
    np. po 1000 stron kończyć tą funkcję.

    :param generator contents: Wynik wywołania funkcji: ``iter_over_contents``,
        czyli generator który zwraca krotki: (tytuł, zawartość artykułu).
    :param int ngram_len: Długość generowanych n-gramów. Jeśli parametr ten
        przyjmie wartość 1 to wyznaczacie Państwo rozkład częstotliwości
        pojawiania się poszczególnyh liter w wikipedii

    :return: Funkcja zwraca słownik n-gram -> ilość wystąpień
    """
    slownik = {}
    iterator2=0
    for line in contents:
        iterator = 0
        #if iterator2 > 1000: break
        #iterator2 += 1
        #print(iterator2)
        while iterator+ngram_len-1 < len(line[1]):
            cos = line[1][iterator:iterator+ngram_len]            
            if cos in slownik:
                slownik[cos] = int(slownik[cos]) + 1
                #print(line[1]+" "+cos)
                #print(len(line[1]))
                #print(iterator)
            else:
                slownik[cos] = 1
                #print(line[1]+" "+cos)
                #print(len(line[1]))
                #print(iterator)
            iterator += 1
    return slownik



def save_ngrams(out_file, contents):
    """
    Funkcja która (tylko) zapisuje n-gramy do pliku.

    Plik ma format csv w dialekcie ``csv.unix_dialect`` i jest posortowany
    względem zawartości n-grama.

    :param dict contents: Słownik z n-gramami
    :param str out_file: Plik do którego n-gramy zostaną zapisane
    """
    slownik = generate_ngrams(contents, 7)
    lista_wyjsciowa = []
    for cokolwiek in slownik:
        lista_wyjsciowa.append((cokolwiek, int(slownik[cokolwiek])))
    lista_wyjsciowa = sorted(lista_wyjsciowa, key=lambda x: x[0])

    with open(out_file, 'w') as out:
        writeFile = csv.writer(out, dialect=csv.unix_dialect)
        writeFile.writerows(lista_wyjsciowa)

