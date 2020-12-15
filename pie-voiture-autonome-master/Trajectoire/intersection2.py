from math import *

def intersection2(p,dir,segment):
    """
Retourne [res,[xinter,yinter]], où res vaut 1 si la droite de direction 'dir' passant par 'p' coupe le segment 'segment'.
xinter et yinter sont l'abscisse et l'ordonnée d'un point intermédiaire utilisé dans les équations de droite qui suivent.

P = [xp, yp]
dir est un entier, représentant l'angle en radian entre l'axe des abscisses et la droite de direction dir
segment = [x1,y1,x2,y2]

ATTENTION, il y a un changement de repère pour le point 1 et 2 de segment:
x1,y1,x2 et y2 sont ajustés comme si le point p était au centre du repère.
(ceci est fait pour pouvoir utiliser 'dir' en tant que simple angle du cercle trigo de centre p)
    """
    xp=p[0]
    yp=p[1]
    x1=segment[0]-xp
    y1=segment[1]-yp
    x2=segment[2]-xp
    y2=segment[3]-yp
    
    # Comme pour intersection.py, on utilise une équation de droite pour trouver l'intersection.
    Kp=tan(dir*2*pi/360)
    res=0
    if x2!=x1:
        K=(y2-y1)/(x2-x1)
        C=y1-K*x1
        if Kp!=K:
            xinter=(C)/(Kp-K)
            yinter=Kp*(C)/(Kp-K)
            if (x1-xinter)*(x2-xinter)+(y1-yinter)*(y2-yinter)<=0:
                res=1
        if Kp==K:
            res=0
            [xinter,yinter]=[0,0]
    if x2==x1:
            xinter=x1
            yinter=Kp*xinter
            if (x1-xinter)*(x2-xinter)+(y1-yinter)*(y2-yinter)<=0:
                res=1

    return([res,[xinter,yinter]])