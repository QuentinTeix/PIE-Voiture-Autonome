def traitement(map):
	
	
	n=len(map)
	mapt=[0 for i in range(n)]
	cone=30
	for i in range(n):
		for k in range(-cone,cone):
			mapt[i]+=map[(i+k)%n]
		mapt[i]=mapt[i]/(2*cone+1)
	return mapt
