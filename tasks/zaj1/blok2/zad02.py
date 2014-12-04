def range2(x0, xN, n):
	elem = list(range(n))
	skok = (xN - x0) / (n-1)
	lista = list(range(n))
	for i in elem:
		lista[i] = x0 + i * skok
	return lista


nasza_lista = range2(5, 20, 5)
print(nasza_lista)


