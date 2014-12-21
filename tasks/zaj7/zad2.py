import bs4
import requests
import hashlib
import time 

from multiprocessing.pool import ThreadPool
from multiprocessing import Pool

#ip = "http://194.29.175.134:4444"
ip = "http://127.0.0.1:4444"

data = requests.post(ip +"/login", {'uname': 'foo', 'password':'bar'}, allow_redirects=False)
print("DATA: ", data.cookies)
bs = bs4.BeautifulSoup(data.text)
#print("BEAUTY: " ,bs)
data2 = requests.get(ip +"/numeryindeksowzespolu", cookies=data.cookies)
print("DATA2: ", data2)
bs2 = bs4.BeautifulSoup(data2.text)
print("BEAUTY2: " ,bs2)

