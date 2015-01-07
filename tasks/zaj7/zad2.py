import bs4
import requests
import hashlib
import time 
import numpy as np

#from multiprocessing.pool import ThreadPool
from multiprocessing import Pool, Queue, Process

#ip = "http://194.29.175.134:4444"
ip = "http://127.0.0.1:4444"

data = requests.post(ip +"/login", {'uname': 'foo', 'password':'bar'}, allow_redirects=False)
#print("DATA: ", data.cookies)
bs = bs4.BeautifulSoup(data.text)
#print("BEAUTY: " ,bs)

data2 = requests.get(ip +"/numeryindeksowzespolu", cookies=data.cookies)
#print("DATA2: ", data2)
bs2 = bs4.BeautifulSoup(data2.text)
#print("BEAUTY2: ", bs2)


q_in, q_out = Queue(), Queue()

def process(q_out, q_in):
    #while True:
        #temp = q_in.get()
        #print("process",temp)
        #data = requests.get(ip +temp[0], cookies=data2.cookies)
        #bs = bs4.BeautifulSoup(data.text)
        #for a in bs.find_all('a', href=True):
            #q_out.put([a['href'], temp[1]+1])
    print(q_in.get())
    page_to_be_searched = []
    while np.logical_not(q_in.empty()):
        if q_in.empty()==False:
            page_to_be_searched.append(q_in.get())
            print("33", page_to_be_searched)
    for i in page_to_be_searched:
        if i[1]<5 :
            data = requests.get(ip +i[0], cookies=data.cookies)
            bs = bs4.BeautifulSoup(data.text)
            for a in bs.find_all('a', href=True):
                q_out.put([a['href'], i[1]+1])

links = []
data = requests.get(ip +"/numeryindeksowzespolu", cookies=data2.cookies)
bs = bs4.BeautifulSoup(data.text)
for a in bs.find_all('a', href=True):
    links.append([a, 1])
    q_out.put([a['href'], 1])

processes = []
for i in range(4):
    p = Process(target=process, args=(q_in, q_out))
    p.start()
    processes.append(p)


#while np.logical_not(q_in.empty()):
while True:
    print("1")
    temp = q_in.get(timeout=1.0)
    print(temp)
    if temp[1]<5:
        q_out.put([temp[0], temp[1]])
    else:
        links.append([temp[0], temp[1]])


for p in processes:
    p.terminate()
print(links)


