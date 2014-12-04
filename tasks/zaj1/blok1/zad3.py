import math

N = 100000
stala = 2 * math.pi / N
sinus = {}
for i in range(N):
	x = round(stala * i , 3)	
	sinus [x] = round(math.sin(x), 3)
print(sinus)
