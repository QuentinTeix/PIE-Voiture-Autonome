#simulation de trajectoire:
import matplotlib.pyplot as plt
import numpy as np
import copy
from zonesafe import *
from adaptevitesserelat import *
from trouvecible import *
from environment import *
from lidar import *
from actualise import *
from actualise2 import *
from paramètres import *
from calculrayoncourbure import *
from math import *
from objectif import *

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation

"""
Ce module a été recodé afin de permettre une visualisation de la trajectoire de la voiture 
dans le but de verifier le bon fonctionement des algorithmes 

Il suffit de completer la zone - A REMPLIR - avec le code permettant de passer d'une 
position a une autre puis de lancer le programme 

"""


#creation environement et initialisation variables
envir=environment()
[positioninit,orientationinit,vinit,deltat,amaxlat,epsilonmax,amax,amin,tsb,l,larg,vmax,N,rv,m,alpha,lanti]=params()
alphainc=360/N   #angle incrementation lidar
orientation=0
v=vinit
positionm1=[11.3,-8]
orientationm1=0
vm1=vinit


#on creer la figure et on l'initialise
fig = plt.figure()
plt.axis('equal')
plt.grid()


def tracer_env(envir) : 
    """ 
    fonction permettant de remettre a neuf l'environement 
    """
    plt.clf()
    n=len(envir)
    i=0
    while i<n:
        nn=len(envir[i])
        j=0
        while j<(nn-1):
            plt.plot([envir[i][j][0],envir[i][j+1][0]],[envir[i][j][1],envir[i][j+1][1]],"c:o")
            j+=1
        i+=1

 
# ----------- ANIMATION -----------

t = 0
dt = 0.1 #pas de temps 

for k in range(8) : 

    #affichage de l'environement clean     
    tracer_env(envir)



    # ------------- A REMPLIR ----------------#

    #calcul position actuelle du vehicule
    pos_x = [1 , 2, 3, 4, 5, 6, 7, 8]
    pos_y = [-1,-1,-1,-1,-1,-1,-1,-1.2]
    yaw =   [0 , 0, 0, 0, 0, 0, 0,-45]

    position=[pos_x[k],pos_y[k]]
    x = position[0]
    y = position[1]
    orientation = yaw[k]

    #mesure du lidar 
    M = lidar(envir,position,orientation,N)

    #calcul zone safe 
    MMMR = zonesafe(M,rv,m)
   
    # ------------- A REMPLIR ----------------#



    #creation et positionement d'un patch representant la voiture
    patch = patches.Rectangle((0, 0), 0, 0, fc='y')
    ax = fig.add_subplot(111)    
    ax.add_patch(patch)    
    patch.set_width(0.8)
    patch.set_height(0.5)
    patch.set_xy(position) #modification position
    patch.angle = orientation      #modification angle


    #tracé de ce que voit le lidar 
    i = 0
    while i < len(MMMR):
        #abscisse du point BORDURE mesuré dans ref lidar 
        xl=MMMR[i][2] 
        yl=MMMR[i][3]

        #calcul angle du point mesuré a partir increment 
        theta=MMMR[i][0]  
        thetac=(theta*alphainc+orientation)*2*pi/360  #angle de coord polaires dans le ref absolu
        
        #distance du point BORDURE au lidar 
        r=MMMR[i][1]

        #coordonné du point BORDURE dans le referentiel absolu 
        xlc=r*cos(thetac)+x #rcos(thetac) =abscisse dans le ref du lidar rotationné de orientation xlc=abscisse dans le ref absolu
        ylc=r*sin(thetac)+y

        #coordonné du point dans le referentiel lidar ZONE SAFE
        xlp=MMMR[i][4] 
        ylp=MMMR[i][5]
 
        #calcul angle du point mesuré ZONE SAFE  
        if (xlp != 0) :
            thetap=atan((ylp)/(xlp))
        if xlp<0:
            thetap=pi+atan(ylp/xlp)
        thetacp=thetap+orientation*2*pi/360

        #calcul distance entre lidar et point zone safe ref absolu 
        rp=sqrt(xlp**2+ylp**2)
        xlpc=rp*cos(thetacp)+x
        ylpc=rp*sin(thetacp)+y

        #y a plus qu'a afficher !         
        plt.plot(xlc, ylc,"b:o")
        plt.plot(xlpc,ylpc,"r:o")    
        i+=1

    #recherche de la cible
    if (trouvecible(MMMR) == "ERREUR") :
        continue
    
    cible_value = trouvecible(MMMR)
    xl=cible_value[2] 
    yl=cible_value[3]

    #calcul angle du point mesuré a partir increment 
    theta=cible_value[0]  
    thetac=(theta*alphainc+orientation)*2*pi/360  #angle de coord polaires dans le ref absolu
    
    #distance du point BORDURE au lidar 
    r=cible_value[1]

    #coordonné du point BORDURE dans le referentiel absolu 
    xlc=r*cos(thetac)+x #rcos(thetac) =abscisse dans le ref du lidar rotationné de orientation xlc=abscisse dans le ref absolu
    ylc=r*sin(thetac)+y

    #coordonné du point dans le referentiel lidar ZONE SAFE
    xlp=cible_value[4] 
    ylp=cible_value[5]

    #calcul angle du point mesuré ZONE SAFE  
    if (xlp != 0) :
        thetap=atan((ylp)/(xlp))
    if xlp<0:
        thetap=pi+atan(ylp/xlp)
    thetacp=thetap+orientation*2*pi/360

    #calcul distance entre lidar et point zone safe ref absolu 
    rp=sqrt(xlp**2+ylp**2)
    xlpc=rp*cos(thetacp)+x
    ylpc=rp*sin(thetacp)+y

    #y a plus qu'a afficher !         
     
    plt.plot(xlpc,ylpc,"k:o")
    plt.plot([xlc, x],[ylpc, y])    

    plt.pause(dt)
    t = t + dt 


        
 
 


    
plt.axis('equal')
plt.show()
    
#il y a des pb de sortie de piste, je soupçonne l'algo de calcul de rayon de courbure (pb de ref lidar) ou l'algo d'actualisation des données... plutot l'actualisation! 
#visiblement l'ajustement en fct de v bugue a cause du mauvais callage? a cause de actu? a cause du prgm lui mm? param alpha réglé à 0 pour éliminer le pb pour le moment 
#je regarde vers le bas mais je monte... y a un pb dans actu
#actu est codée avec le cul pour actualiser la position, va falloir trouver mieux 
    
