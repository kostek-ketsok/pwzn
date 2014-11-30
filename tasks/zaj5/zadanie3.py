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
    #print(data)
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
    
    polozenia = np.array(data['particle_position'])
    masa = np.array(data['particle_mass'])
    masa_calkowita = masa.sum(axis=0)
    polozenie_suma = np.zeros((len(polozenia[:,0]), 3))
    polozenie_suma = polozenia[:, :] * masa[:, np.newaxis]
    polozenie_suma2 = polozenie_suma.sum(axis=0)
    #print(masa)
    #print(masa_calkowita)
    print(polozenia)
    #print(polozenie_suma2[0])
    return (polozenie_suma2[0]/masa_calkowita, polozenie_suma2[1]/masa_calkowita, polozenie_suma2[2]/masa_calkowita)


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
    v = data['particle_velocity'][:]
    m = data['particle_mass'][:]
    v2 = v[:, 0]*v[:, 0]
    v2_dlugosc = v2[:,0]*v2[:,0] + v2[:,1]*v2[:,1] + v2[:,2]*v2[:,2]
    ekin = 0.5 * v2_dlugosc[:, np.newaxis] * m[:]

    #print("ekin=", ekin,"\nmasa=", m[0:3], "\nv2=",v2_dlugosc[:])
    ekin2 = []
    for i in ekin:
        if i[0] > left:
            if i[0] < right:
                ekin2.append(i[0])
    ekin2 = sorted(ekin, key=lambda x: x[0])
    wartosci, biny = np.histogram(ekin2, bins)
    #print(wartosci)
    return wartosci
    

if __name__ == "__main__":
    data = load_data("...")
    # print(data['velocity'])
    print(get_event_count(data))
    print(get_center_of_mass(1, data))
    print(list(get_energy_spectrum(3, data, 0, 90, 100)))
