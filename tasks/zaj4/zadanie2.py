# -*- coding: utf-8 -*-

import numpy as np

from itertools import chain, permutations, product


def calculate_neighbours(board):

    """

    Funkcja zwraca tablicę która w polu N[R, C] zwraca ilość sąsiadów którą 
    ma komórka Board[R, C]. Za sąsiada uznajemy obszazoną komórkę po bokach lub
    na ukos od danej komórki, komórka nie jest swoim sąsiatem, zatem maksymalna
    ilość sąsiadów danej komórki wynosi 8.

    Funkcja ta powinna być zwektoryzowana, tj ilość operacji w bytekodzie
    Pythona nie powinna zależeć od rozmiaru macierzy.

    :param np.ndarray board: Dwuwymiarowa tablica zmiennych logicznych która
    obrazuje aktualny stan game of life. Jeśli w danym polu jest True (lub 1)
    oznacza to że dana komórka jest obsadzona


    Podpowiedź: Czy jest możliwe obliczenie ilości np. lewych sąsiadów
    których ma każda z komórek w macierzy, następnie liczymy ilość sąsiadów
    prawych itp.

    Podpowiedź II: Proszę uważać na komówki na bokach i rogach planszy.
    """
    kolumnyBoard = len(board[0,:])
    wierszeBoard = len(board[:,0])
    nasza = np.zeros((wierszeBoard, kolumnyBoard))
    nasza[:, 1:kolumnyBoard] += board[:, 0:(kolumnyBoard-1)]
    nasza[:, 0:(kolumnyBoard-1)] += board[:, 1:kolumnyBoard]
    nasza[1:wierszeBoard, :] += board[0:(wierszeBoard-1), :]
    nasza[0:(wierszeBoard-1), :] += board[1:wierszeBoard, :]
    
    nasza[0:(wierszeBoard-1), 0:(kolumnyBoard-1)] += board[1:wierszeBoard, 1:kolumnyBoard]
    nasza[1:wierszeBoard, 1:kolumnyBoard] += board[0:(wierszeBoard-1), 0:(kolumnyBoard-1)]
    nasza[0:(wierszeBoard-1), 1:kolumnyBoard] += board[1:wierszeBoard, 0:(kolumnyBoard-1)]
    nasza[1:wierszeBoard, 0:(kolumnyBoard-1)] += board[0:(wierszeBoard-1), 1:kolumnyBoard]
    
    return nasza


def iterate(board):

    """

    Funkcja pobiera planszę game of life i zwraca jej następną iterację.

    Zasady Game of life są takie:

    1. Komórka może być albo żywa albo martwa.
    2. Jeśli komórka jest martwa i ma trzech sąsiadóœ to ożywa.
    3. Jeśli komórka jest żywa i ma mniej niż dwóch sąsiadów to umiera,
       jeśli ma więcej niż trzech sąsiadóœ również umiera. W przeciwnym wypadku
       (dwóch lub trzech sąsiadów) to żyje dalej.

    :param np.ndarray board: Dwuwymiarowa tablica zmiennych logicznych która
    obrazuje aktualny stan game of life. Jeśli w danym polu jest True (lub 1)
    oznacza to że dana komórka jest obsadzona

    """
    sasiedzi = calculate_neighbours(board)
    np.logical_and((board[:,:] == False), (sasiedzi[:,:] == 3))
       # board[:,:] = True
    np.logical_and(np.logical_not((board[:,:] == True), np.logical_or((sasiedzi[:,:]<2), (sasiedzi[:,:]>3))))
       # board[:,:] = False
    return board
    
    

    
