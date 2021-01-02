from math import *


def actualise(R,v,position,obj,orientation,deltat,amaxlat,epsilonmax,amax,amin,tsb,l,vmax,N):
    """
    Cette fonction met à jour la position, l'orientation et la vitesse du mobile.

    Arguments de la fonction :
    R -> Rayon actuel de courbure
    v -> vitesse du mobile
    position = [x, y] -> position absolue du mobile dans le référenciel de base
    obj = [xobj, yobj] -> position d'un obstacle dans le référenciel de base
    orientation -> (du véhicule ?) c'est un angle

    Les variables suivantes sont des constantes définies dans les paramètres
    deltat = 1/24
    amaxlat = 20 (a = accélération ? lat = latitude ?)
    amax = 2
    amin = -2
    epsilonmax = 45
    tsb = 0.1
    l=0.4
    vmax = 30/3.6
    N = 720
    """
    # Mise à jour du rayon de courbure (R devient le max de quelque chose d'inconnu pour le moment...)
    R=abs(R)
    Rprim = max(R, tsb*v**2/(epsilonmax*2*pi/360) + l/(epsilonmax*2*pi/360), sqrt(v**2/amaxlat))

    # récupération des coordonnées de l'obstacle
    xobj=obj[0]
    yobj=obj[1]  
   
    # calcul des coordonnées du point atteint apres deltat dans le référenciel du lidar
    xprim=0
    yprim=0
    xprim1=0
    yprim1=0
    thetaparc=0
    if v!=0:
        thetaparc = atan(xobj/(Rprim-abs(yobj)))
        yprim = Rprim*(1-cos(thetaparc))
        xprim = (Rprim-yprim)*sin(thetaparc)
        
        if yobj<0:
            yprim=-yprim
           
        #débugage
        #thetaparc=atan(yobj/xobj)
        #xprim=xobj
        #yprim=yobj  
        print('xobj',xobj)
        print('yobj',yobj)
        print('xprim',xprim)
        print('yprim',yprim)
        
        
        
        rprim = sqrt(xprim**2 + yprim**2)
        
        alphainc=360/N
        xprim1 = rprim*cos(thetaparc + orientation*2*pi/360) #correction en angle? 
        yprim1 = rprim*sin(thetaparc + orientation*2*pi/360)
        
    
    # calcul des coordonnées du point atteint après deltat dans le référenciel absolu
    xabs = xprim1 + position[0]
    yabs = yprim1 + position[1]
    
    positionprim = [xabs,yabs]
    
    # calcul de la nouvelle orientation
    # (le mobile a commencé a tourné en suivant le rayon de courbure ? C'est peut-être pour cela que l' orientation et à remettre à jour)
    alphainc = 360/N
    orientationprim = orientation + thetaparc*360/(2*pi)
    #if obj[1]<position[1]:
    #    orientationprim=orientation-thetaparc
    #calc nouvelle vitesse
    
    vmaxr = sqrt(amaxlat*Rprim)
    a = min(1,(vmaxr-v)/(deltat*amax))*amax
    if v>vmaxr:
        a = min(1,(vmaxr-v)/(deltat*amin))*amin     # accélératon <= 1
    
    vprim = min(vmax,v+a*deltat)
    
    return(positionprim,orientationprim,vprim)
