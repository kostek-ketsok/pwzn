import requests
import hashlib
import time 

from multiprocessing.pool import ThreadPool
from multiprocessing import Pool

def finezyjnie(sciezka, iloscWatkow):
    dataOUT = []
    dataHEAD  = requests.head(sciezka)
    dataLenght = int(dataHEAD.headers['Content-Length'])
    step = int(dataLenght/iloscWatkow)
    
    #print(dataLenght/1024/1024, "MB")

    for ii in range(0, dataLenght, step): 
        request_range = (ii, min(dataLenght, ii+step-1))
        #print(request_range)   
        response = requests.get(sciezka, 
                     headers = {
                        "Range": "bytes={}-{}".format(*request_range)
                    })
        dataOUT.append(response)
    collected = b"".join([d.content for d in dataOUT])
    hash = hashlib.md5()
    hash.update(collected)
    hash.hexdigest()
    print("HASH pliku pobranego : ", hash.hexdigest())
    return dataOUT


def jedenFragment(arg):
    #print(arg)
    sciezka, iloscWatkow, numerWatku = arg
    dataHEAD  = requests.head(sciezka)
    dataLenght = int(dataHEAD.headers['Content-Length'])
    step = int(dataLenght/iloscWatkow)
    request_range = (step*numerWatku, min(dataLenght, step*numerWatku+step-1))
    #print(request_range)  
    response = requests.get(sciezka, 
        headers = {
            "Range": "bytes={}-{}".format(*request_range)
        })
    return response


def wieloprocesorowo(sciezka, iloscWatkow):  
    p = ThreadPool(iloscWatkow)
    data=[]
    for ii in range(0, iloscWatkow+1):
        krotka = (sciezka, iloscWatkow, ii)
        data.append(krotka)
    #print(data)

    try:
        start = time.monotonic()
        result = p.map(jedenFragment, data)
        print(time.monotonic() - start)
    finally: 
        p.close()
        p.join()
    
    collected = b"".join([d.content for d in result])
    hash = hashlib.md5()
    hash.update(collected)
    print("HASH pliku pobranego2: ", hash.hexdigest())


finezyjnie("http://db.fizyka.pw.edu.pl/pwzn-data/zaj7/rand-data-a", 11)
wieloprocesorowo("http://db.fizyka.pw.edu.pl/pwzn-data/zaj7/rand-data-a", 11)



