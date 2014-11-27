# -*- coding: utf-8 -*-

from tasks.zaj5.zadanie2 import  load_data # Musi tu być żeby testy przeszły

import numpy as np


def get_event_count(data):
    """

    Dane w pliku losowane są z takiego rozkładu:
    position, velocity: każda składowa losowana z rozkładu równomiernego 0-1
    mass: losowana z rozkładu równomiernego od 1 do 100.

    Zwraca ilość zdarzeń w pliku. Każda struktura ma przypisane do którego
    wydarzenia należy. Jeśli w pliku jest wydarzenie N > 0
    to jest i wydarzenie N-1.

    :param np.ndarray data: Wynik działania zadanie2.load_data
    """
    return max(data['event_id'][:])


def get_center_of_mass(event_id, data):
    """
    Zwraca macierz numpy zawierajacą położenie x, y i z środka masy układu.
    :param np.ndarray data: Wynik działania zadanie2.load_data
    :return: Macierz 3 x 1
    """

    #event_table = np.array(data['event_id'][:])
    #indeksy = np.where(event_table == event_id)
    ##masa_calkowita = 0
    #polozenia = np.array((np.max(indeksy), 3))
    #masa = np.array((np.max(indeksy)))
    #for i in indeksy:
        ##masa_calkowita += data[i][2]
        #polozenia[i, 0] = data[i, 2][0]
        #polozenia[i, 1] = data[i, 2][1]
        #polozenia[i, 2] = data[i, 2][2]
        #masa[i]=data[i][2]

    polozenia = np.array(data['particle_position'][:])
    masa = np.array(data['particle mass'][:])
    masa_calkowita = masa.sum(axis=0)
    polozenie_suma = np.array(polozenia[:, :] * masa[:, np.newaxis]).sum(axis=0)
    return (polozenie_suma[0]/masa_calkowita, polozenie_suma[1]/masa_calkowita, polozenie_suma[2]/masa_calkowita)


def get_energy_spectrum(event_id, data, left, right, bins):
    """
    Zwraca wartości histogramu energii kinetycznej cząstek (tak: (m*v^2)/2).
    :param np.ndarray data: Wynik działania zadanie2.load_data
    :param int left: Lewa granica histogramowania
    :param int right: Prawa granica historamowania
    :param int bins: ilość binów w historamie
    :return: macierz o rozmiarze 1 x bins

    Podpowiedż: np.histogram
    """
    masa = np.array(data['particle mass'][:])
    predkosc =  np.array(data['particle_velocity'][:])
    ekin = np.array(0.5 * masa[:] * np.sqrt(predkosc[:,0] * predkosc[:,0] + predkosc[:,1] * predkosc[:,1] + predkosc[:,2] * predkosc[:,2]))
    ekin2 = []
    for i in ekin:
        if (i >= left) | (i<=right):
            ekin2.append(i)
    wartosci, biny = np.histogram(ekin2, bins)
    print(wartosci)
    return wartosci
    

if __name__ == "__main__":
    data = load_data("...")
    # print(data['velocity'])
    print(get_event_count(data))
    print(get_center_of_mass(1, data))
    print(list(get_energy_spectrum(3, data, 0, 90, 100)))
