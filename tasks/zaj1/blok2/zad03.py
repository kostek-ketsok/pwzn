import math

def furier(furier_arg, points, rozklad):
	if rozklad == "cos":
		y = 0;
		iteracjaX = 0
		wynik = [None]*len(points)
		for x in points:
			iteracja = 0;	
			for c in furier_arg:	
				y += c*math.cos(iteracja*x)
				iteracja += 1 
			wynik[iteracjaX] = y
			iteracjaX+=1
		return wynik
		pass
	if rozklad == "sin":
		y = 0;
		iteracjaX = 0
		wynik = [None]*len(points)
		for x in points:
			iteracja = 0;	
			for c in furier_arg:	
				y += c*math.sin(iteracja*x)
				iteracja += 1 
			wynik[iteracjaX] = y
			iteracjaX+=1
		return wynik
		pass

furierowskie = furier(range(5), (1,2,3), "cos")
print(furierowskie)
