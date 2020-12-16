from math import *
import copy

"""
//Ancienne notations des variables//
tab_dist --> M
tab_dist_front --> MR
tab_dist_front_cart --> MMR
environment --> MMMR
"""

def zonesafe (tab_dist,rv,m):
    """
    Fonction qui détermine la zone 'interdite' (dans laquelle il ne faut pas aller pour éviter de toucher le bord) à partir des bords de l'environnement, donné par le lidar.
    Cette fonction RENVOIE 'environment', expliqué ensuite.

    tab_dist : Tableau qui contient les données du lidar, ie: les distances 'ri' aux obstacles pour chaques angles 'thetai'; tab_dist=[(thetai,ri)]
    (attention thetai n'est pas vraiment un angle mais plutot le numéro de la capture de distance effectuées par le lidar (qui mesure les distances en tournant sur lui-même) depuis la position de réfèrence)
    (pour avoir l'angle on fera : angle = thetai*2*pi/N , où N est le nombre de mesures effectuées par le lidar)
    tab_dist_front = [(thetai,ri)]

    rv : Rayon du cercle circonscrit au véhicule.

    m : Marge en plus du cercle circosncrit au véhicule.

    Dans la suite on utilisera:
    tab_dist_front : tout ce qui concerne le devant de la voiture dans tab_dist (sachant que 0 degré est au Nord).
    tab_dist_front = [(thetai,ri)]

    tab_dist_front_cart : tab_dist_front en coordonnées cartésiennes (toujours par rapport à la position actuelle; le lidar est en (0,0)).
    tab_dist_front_cart = [(thetai,ri,xi,yi)]

    environment : tab_dist_front_cart auquel est ajouté le point qui délimite la zone 'safe'. Entre ce point et le bord c'est la zone où il ne faut pas aller
    environment = [(thetai,ri,xi,yi,xpi,ypi)]
    """
        
    N = len(tab_dist)
    A = copy.deepcopy(tab_dist[0:int(N/4)])      # on prend le quart de cercle de devant à gauche (le O degré est au Nord)
    B = copy.deepcopy(tab_dist[int(3*N/4):N])    # quart de cercle de deant à droite
    A.reverse()                 # sinon A[0] est la mesure en face et A[-1] celle de gauche
    B.reverse()                 # sinon B[0] est la mesure à droite et B[-1] celle presque en face
    tab_dist_front = copy.deepcopy(A+B)

    tab_dist_front_cart=[]
    i = 0
    while i<len(tab_dist_front):        # len(tab_dist_front) = N/2 à peu près...
        theta = tab_dist_front[i][0]
        r = tab_dist_front[i][1]
        xi = r*cos(theta*2*pi/N)
        yi = r*sin(theta*2*pi/N)
        tab_dist_front_cart.append([theta,r,xi,yi])
        i = i+1
    
    environment=[] 
    i=1
    while i<(len(tab_dist_front_cart)-1):
        xim1 = tab_dist_front_cart[i-1][2]  # abscisse du point 'i moins 1' (précédent)
        yim1 = tab_dist_front_cart[i-1][3]
        xi = tab_dist_front_cart[i][2]
        yi = tab_dist_front_cart[i][3]
        xip1 = tab_dist_front_cart[i+1][2]  # abscisse du point 'i plus 1' (suivant)
        yip1 = tab_dist_front_cart[i+1][3]
        
        if abs(yip1-yim1)>0.00001:      # si la droite passant par les point m1 et p1 est peu horizontale
            K = -(xip1-xim1)/(yip1-yim1)  # K est le coefficient directeur de la droite T orthogonale à (im1,ip1) ie: orthogonale au bord du circuit.
            C = yi-K*xi                   # y = Kx+C

            # abscisse et ordonnée du point sur la droite T distant de rv+m du point i
            xp1 = xi+(rv+m)/sqrt(1+K**2) 
            yp1 = yi+K*(rv+m)/sqrt(1+K**2)
        
            # abscisse et ordonnée du point sur la droite T distant de rv+m du point i (mais de l'autre côté de la droite)
            xp2 = xi-(rv+m)/sqrt(1+K**2)
            yp2 = yi-K*(rv+m)/sqrt(1+K**2)

        if abs(yip1-yim1)<0.00001:      # si la droite passant par les point m1 et p1 est quasi horizontale
            yp1 = yi+rv+m
            yp2 = yi-(rv+m)
            xp1 = xi
            xp2 = xi
        
        """
        Utiliser K pour faire la suite, plutôt que des distances... A voir...
        """

        d1 = (xp1)**2+(yp1)**2          # distance du lidar au point p1
        d2 = (xp2)**2+(yp2)**2
            
        if d1<=d2:                      # si le lidar est plus prche de p1 que de p2 (ie: si p1 est le point dans le terrain)
            environment.append(tab_dist_front_cart[i]+[xp1,yp1])        # on garde p1
        if d1>d2:
            environment.append(tab_dist_front_cart[i]+[xp2,yp2])
        
        i=i+1
    
    return(environment)
    
    
    
    