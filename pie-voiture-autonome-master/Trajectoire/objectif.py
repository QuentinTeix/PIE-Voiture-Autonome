from math import *
"""
Distance pouvant être parcourue en fonction des coordonnées d'une cible, de la vitesse v et d'un temps deltat
"""
def objectif(cible,v,deltat):
    K=atan(cible[1]/cible[0])
    xo=v*deltat/sqrt(1+K**2)
    yo=K*xo
    return([xo,yo])
