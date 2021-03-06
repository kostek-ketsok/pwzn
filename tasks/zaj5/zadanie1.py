# -*- coding: utf-8 -*-
from numpy import char


import mmap
import struct
import numpy as np

def next_item(input):
    """
    Zwraca "następny" ngram dla podanego n-gramu. Działa to dla ciągów znaków ASCII.
    To jest hak, ale działa.

    Można zaimplementować to lepiej.
    :param input:
    :return:
    """
    return input[:-1] + chr(ord(input[-1])+1)


def load_data(path):
    """
    Funkcja która ładuje dane z pliku zawierającego ngramy. Plik ten jest
    plikiem binarnym zaiweającym N wieszy w każdym wierszu jest 7 bajtów 
    zawierających 7-gram a następie czterobajtowa liczba całkowita zawierającą 
    ilość zlieczeń.

    Funkcja zwraca tablicę numpy. Tablica ja jest tylko do odczytu.

    Podpowiedźź: starczą dwie linikji kodu definicja dtype oraz otwarcie macierzy.
    Typ danych jest złożony --- należy użyć Structured Array.
    """
    dtype = np.dtype([
        ("7gram", np.dtype("a7")),
        ('calkowita', np.uint32)])

    data = np.memmap(path, dtype=dtype, mode='r')
    return data

def suggester(input, data):
    """
    Funkcja która sugeruje następną literę ciągu ``input`` na podstawie n-gramów
    zawartych w ``data``.

    :param str input: Ciąg znaków o długości 6 znaków. **UWAGA** W zajęciach trzecich
                      input mógł mieć dowolną długość.
    :param np.ndarray data: Wynik działania ``load_data``.
    :return: Dowolną strukturę którą można zaindeksować w następującyc sposób:
            ret[0][0] zwraca najbardziej prawdopodobną nasßępną literę. ret[0][1]
            jej prawdopodobieństwo. ret[-1][0] zwraca najmniej prawdopodobną literę.
            Dane posortowane są względem prawodpodobieństwa, dane o tym samym prawdopodbieństwie
            są sortowane po kolei.

    By wygenerować częstotliwości należy:

    Dla ustalenia uwagi zakładamy ze input zawiera ciąg znaków `foo`

    1. Znaleźć "następny" n-gram. Krótka funkcja "hak", która zwraca następny
       n-gram jest z
    2. Odnaleźć pierwsze i ostatnie wystąpienie ngramu rozpoczynającego się od wartości
       ``foo``.
    3. Wyznaczyć prawdopodobieństwo wystąpienia kolejnej litery, posortować i zwrócić.

    Przykład zastosowania:

    >>> data = load_data("path")
    >>> suggester('ąęćś', data)
    []
    >>> suggester('pytho', data)
    [('n', 1.0)]
    >>> suggester('pytho', data)
    [('o', 0.7794117647058824),
     ('a', 0.1323529411764706),
     ('e', 0.07352941176470588),
     ('i', 0.014705882352941176)]
    """
    zwracana_tablica = []
    ppo = []
    it = 0
    sumowanie = 0
    chararrey = data['7gram'][:]
    wystapienia = data['calkowita'][:]
    for elem in chararrey:
        if elem.startswith(input.encode('ascii')):
            zwracana_tablica.append((chr(elem[-1]), wystapienia[it]))
            sumowanie = sumowanie + int(wystapienia[it])
        it += 1

    for mel in zwracana_tablica:
        prawdopodobienstwo = int(mel[1])/sumowanie
        ppo.append((mel[0], prawdopodobienstwo))
    ppo = sorted(ppo, key=lambda x: x[0], reverse=True)
    ppo = sorted(ppo, key=lambda x: -x[1])
    return ppo
    
    
#data = lo_data("/opt/pwzn/zaj5/enwiki-20140903-pages-articles_part_0.xmlascii.bin") 
#print(data.shape)   
#print(data['7gram'][0:10])    
#print(suggester('kot', data))


