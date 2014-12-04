i=0
def key(x):
	global i 
	i+=1
	return x

lista = [2, 5, 7, 8, 6, 81, 4, 2, 1, 20, 51, 45, 76, 865, 0]

lista = sorted(lista, key=key)
print(lista)
print(i)
