import numpy as np
import random
data = np.asarray([random.uniform(0,1000) for ii in range(10000)], dtype = np.float32)
import time 
import pyximport; pyximport.install()
import zad1

start = time.monotonic()
zad1.quicksort(data, 0, 10000-1)
print(time.monotonic() - start)

