# -*- coding: utf-8 -*-
import csv
from collections import defaultdict

def merge(path1, path2, out_file):
    """
    Funkcja pobiera nazwy dwóch plików z n-gramami (takie jak w poprzedmim
    zadaniu) i łączy zawartość tych plików i zapisuje do pliku w ścieżce ``out``.

    Pliki z n-gramami są posortowane względem zawartości n-grama.

    :param str path1: Ścieżka do pierwszego pliku
    :param str path2: Ścieżka do drugiego pliku
    :param str out_file:  Ścieżka wynikowa

    Testowanie tej funkcji na pełnych danych może być mało wygodne, możecie
    stworzyć inną funkcję która działa na dwóch listach/generatorach i testować
    ją.

    Naiwna implementacja polegałaby na stworzeniu dwóch słowników które
    zawierają mapowanie ngram -> ilość wystąpień i połączeniu ich.

    Lepsza implementacja ładuje jeden z plików do pamięci RAM (jako słownik
    bądź listę) a po drugim iteruje.

    Najlepsza implementacja nie wymaga ma złożoność pamięciową ``O(1)``.
    Podpowiedź: merge sort. Nie jest to trywialne zadanie, ale jest do zrobienia.
    """
    with open(path1, 'r') as file1, open(path2, 'r') as file2, open(out_file, 'w') as out:
        readFile1 = csv.reader(file1, dialect=csv.unix_dialect)
        readFile2 = csv.reader(file2, dialect=csv.unix_dialect)
        writeFile = csv.writer(out, dialect=csv.unix_dialect)

        slownik = defaultdict(lambda : 0)
        for line in readFile1:
            slownik[line[0]] = line[1]

        for line in readFile2:
            if line[0] in slownik:
                slownik[line[0]] = int(slownik[line[0]]) + int(line[1])
            else:
                slownik[line[0]] = line[1]
        
        lista_wyjsciowa = []
        for cokolwiek in slownik:
            lista_wyjsciowa.append((cokolwiek, int(slownik[cokolwiek])))
        lista_wyjsciowa = sorted(lista_wyjsciowa, key=lambda x: x[0])

        writeFile.writerows(lista_wyjsciowa)

if __name__ == '__main__':

    merge(
        '/opt/pwzn/zaj3/enwiki-20140903-pages-articles_part_0.xmlascii.csv',
        '/opt/pwzn/zaj3/enwiki-20140903-pages-articles_part_1.xmlascii.csv',
        '/tmp/mergeout.csv')