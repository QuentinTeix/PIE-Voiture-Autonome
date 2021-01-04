import matplotlib.pyplot as plt
import numpy as np
import copy
from zonesafe import *
from adaptevitesserelat import *
from trouvecible import *

"""
Ce module a pour objectif de faire un tracer afin de verifier le bon fonctionement de trouvecible.
Il considere lidar1 et lidar2 comme etant les mesures du lidar 
Il trace :
    - le bord du parcours en bleu 
    - la zone safe facile en rouge 
    - la zone safe adapte entre les angle -alpha et alpha en vert
    - la cible trouvée


environment --> MMMR [(thetai,ri,xi,yi,xpi,ypi)]
environment_adapte --> MMMRC  [(thetai,ri,xi,yi,xpi ou xpiprim,ypi ou ypiprim)]
"""

#on sait pas a quoi ca sert
orientation=0
orientationm1=0

#Nombre d'angle de mesure du lidar
N=720
#rayon cercle circonscrit
rv=20
# marge 
m=5

#sert a corriger zone safe selon vitesse mais on comprend pas super bien encore
epsilon=0.15
alpha=15 #hyper important corrige que ce qui est compris entre -alpa et alpa !!
v=100
deltat=0.1
rmax=1000

# on simule les mesures on rappel que le lidar est en position (0,0)
# toutes les mesures sont situé a une distance r1 et ré du lidar donc on a des arc de cercle 
lidar1=[]
r1=50
lidar2=[]
r2=41

i=0
while i<N:
    lidar1.append((i,r1))
    i+=1
i=0
while i<N:
    lidar2.append((i,r2))
    i+=1
    
#on calcul zone safe 
environment=zonesafe(lidar2,rv,m)
#on calcul zone safe avec dapatation vitesse
environment_adapte=adaptevitesserelat (lidar1,lidar2,environment,alpha,v,deltat,rmax,orientation,orientationm1)
#on cherche la cible
cible=trouvecible(environment_adapte)

#on trace tout ca 
i=0
while i<len(environment):
	#en bleu le bord du circuit
    plt.plot(environment[i][2], environment[i][3],"b:o")
    #en rouge la zone safe non adapté a vitesse
    plt.plot(environment[i][4], environment[i][5],"r:o")
    #en vert la zone safe adapté selon la vitesse 
    plt.plot(environment_adapte[i][4], environment_adapte[i][5],"g:o")
    i=i+1


plt.plot(cible[0],cible[1],"y:o")
plt.axis('equal')
plt.show()

#trouvecible testé avec succés
