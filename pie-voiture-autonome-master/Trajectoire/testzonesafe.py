
import matplotlib.pyplot as plt
import numpy as np
import copy
from zonesafe import *

"""
Ce module permet de tester le bon fonctionement de la zone safe avant de tester le bon fonctionement de trouvecible
environment=[(thetai,ri,xi,yi,xpi,ypi)]

"""
#Nombre d'angle de mesure du lidar
N=720
#rayon cercle circonscrit
rv=20
# marge 
m=5

#on remplit liste valeurs lidar toute mesure situé a distance r donc on a arc de cercle
lidar=[]
r=50

i=0
while i<N:
    lidar.append((i,r))
    i+=1

   
#calcul zone safe 
environment=zonesafe(lidar,rv,m)

#on trace 
i=0
while i<len(environment):
    #bord circuit
    plt.plot(environment[i][2], environment[i][3],"b:o")
    #bord zone safe 
    plt.plot(environment[i][4], environment[i][5],"r:o")
    i=i+1
    
plt.axis('equal')
plt.show()

#zonesafe testé avec succés
