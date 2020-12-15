from math import *

def calculrayoncourbure(cible):
    """
Calcule et renvoie le rayon de courbure necessaire pour rejoidre la cible 'cible' depuis zéro en ne prenant comme direction de v la direction dans laquelle pointe le véhicule
cible = [xc,yc]
    """
    xc=cible[0]
    yc=cible[1]

# On va utiliser l'équation de droite (0,cible)
    if yc!=0:
        K=xc/yc         # Pente de la droite (O,cible)
        C=yc/2-K*xc/2
        yo=C
    if yc==0:
        yo=100
    R=yo
    return(R)