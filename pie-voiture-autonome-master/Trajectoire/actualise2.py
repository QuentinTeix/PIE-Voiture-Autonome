from math import *


def actualise2(R,v,position,obj,cible,orientation,deltat,amaxlat,epsilonmax,amax,amin,tsb,l,vmax,N):
    """
    Deuxième version de actualise.py en prenant en compte la cible
    Cette fonction met à jour la position, l'orientation et la vitesse du mobile.

    Arguments de la fonction :
    R -> Rayon actuel de courbure
    v -> vitesse du mobile
    position = [x, y] -> position absolue du mobile dans le référenciel de base
    obj = [xobj, yobj] -> position d'un obstacle dans le référenciel de base
    cible = [x_cible, y_cible]
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
    p=(tsb*vmax+l)/deltat*0.02
    d=p*4.2
    
    theta0 = atan(cible[1]/cible[0])
    theta1 = atan(cible[1]/(cible[0]-v*deltat))
    thetapoint = (theta1-theta0)/deltat
    epsilon = (p*theta0+d*thetapoint)
    #print(epsilon*180/pi)
    epsilon = min(epsilonmax*2*pi/360,epsilon)
    if epsilon<0:
        epsilon = max(-epsilonmax*2*pi/360,epsilon)
        
    # Mise à jour du rayon de courbure (R devient le max de quelque chose de nouveau, mais toujours inconnu...)
    Rprim=abs(tsb*v**2/(epsilon)+l/(epsilon))
   
    # calcul des coordonnées du point atteint apres deltat dans le référenciel du lidar
    xprim=0
    yprim=0
    xprim1=0
    yprim1=0
    thetaparc=0
    if v!=0:
        thetaparc=v*deltat/Rprim
        yprim=Rprim*(1-cos(thetaparc))
        xprim=(Rprim-yprim)*sin(thetaparc)
       
        if cible[1]<0:
            yprim=-yprim            
            thetaparc=-thetaparc
            
        
        #débugage
        #thetaparc=atan(yobj/xobj)
        #xprim=xobj
        #yprim=yobj  
        #print(cible[1])
        #print('thetaparc',thetaparc)
        #print('epsilon',epsilon)
        #print('xobj',obj[0])
        #print('yobj',obj[1])
        #print('xprim',xprim)
        #print('yprim',yprim)
        
        rprim=sqrt(xprim**2+yprim**2)
        
        alphainc=360/N
        xprim1=rprim*cos(thetaparc+orientation*2*pi/360) #correction en angle? 
        yprim1=rprim*sin(thetaparc+orientation*2*pi/360)
        
    
    # calcul des coordonnées du point atteint après deltat dans le référenciel absolu
    xabs = xprim1 + position[0]
    yabs = yprim1 + position[1]
    
    positionprim=[xabs,yabs]
    
    # calcul de la nouvelle orientation
    alphainc = 360/N
    orientationprim = orientation + thetaparc*360/(2*pi)
    #if obj[1]<position[1]:
    #    orientationprim=orientation-thetaparc
    
    #calc nouvelle vitesse (INCOMPREHENSIBLE)
    vmaxr = sqrt(amaxlat*abs(R))
    vmaxant = sqrt(-2/3*amin*(sqrt(cible[0]**2+cible[1]**2)))
    vmaxx = min(vmaxr,vmaxant)
    a = min(1,(vmaxx-v)/(deltat*amax))*amax
    if v>vmaxr:
        a = min(1,(vmaxx-v)/(deltat*amin))*amin
    
    vprim = min(vmax,v+a*deltat)
    
    return(positionprim,orientationprim,vprim)