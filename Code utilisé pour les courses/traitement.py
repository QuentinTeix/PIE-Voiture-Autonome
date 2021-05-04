def traitement(map):
	'''
Cette fonction effectue un moyennage des valeurs de 'map' (les distances)
Elle prend 'cone' valeurs de chaque côté de chaque point de 'map' pour effectuer la moyenne.
On peut considérer cela comme un lissage du bruit.
	'''
	n = len(map)
	mapt = [0 for i in range(n)]
	cone = 30
	for i in range(n):
		for k in range(-cone,cone):
			mapt[i] += map[(i+k)%n]
		mapt[i] = mapt[i]/(2*cone+1)
	return mapt
