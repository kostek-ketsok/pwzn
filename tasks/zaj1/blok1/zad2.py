import math

N = 1000000
lista = range(N)
stala = 2 * math.pi / N
suma = 0

for i in lista:
	suma += math.sin(stala * i) * stala
print(suma)
