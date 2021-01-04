from math import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation
from environment import * 
from zonesafe import *
from lidar import *
from paramètres import *

#creation environement et variables
envir=environment()
[positioninit,orientationinit,vinit,deltat,amaxlat,epsilonmax,amax,amin,tsb,l,larg,vmax,N,rv,m,alpha,lanti]=params()
#angle incrementation lidar
alphainc=360/N
#initialisation grandeur 
position=[2,-1]
orientation=0
v=vinit
positionm1=[11.3,-8]
orientationm1=0
vm1=vinit

#mesure du lidar 
Mm1=lidar(envir,positionm1,orientationm1,N)
M=lidar(envir,position,orientation,N)

#calcul zone safe 
MMMR=zonesafe(M,rv,m)
 




""" 
    ce code sert a simuler une voiture qui se deplace grace aux modules matplotlib.patches 
    et matplotlib.animation 
    
    Pour la voiture on créer un objet patches qui est un rectangle 
"""

#positions succesives de la voiture
x = [0,1,2]
y = [-1,-1,-1]
#angle de la voiture 
yaw = [0, 0, 0]

i=0
alpha=(45+180)*2*pi/360

#centre les positions initiales
while i<len(x):
    x[i]=x[i]+sqrt(2)/2*(cos(yaw[i]*2*pi/360+alpha))
    y[i]=y[i]+sqrt(2)/2*(sin(yaw[i]*2*pi/360+alpha))
    i+=1

#on creer la figure et on l'initialise
fig = plt.figure()
plt.axis('equal')
plt.grid()
ax = fig.add_subplot(111)
ax.set_xlim(-5, 20)
ax.set_ylim(-15, 5)


n=len(envir)
i=0
while i<n:
    nn=len(envir[i])
    j=0
    while j<(nn-1):
        plt.plot([envir[i][j][0],envir[i][j+1][0]],[envir[i][j][1],envir[i][j+1][1]],"c:o")
        j+=1
    i+=1
    
i=0
 
#on creer le patch qui simule la voiture 
patch = patches.Rectangle((0, 0), 0, 0, fc='y')

#fonction d'initialisation qui affiche le patch sur la figure 
def init():
    ax.add_patch(patch)
    plt.plot(1,2, "k:o")
    plt.plot(2,2, "k:o")
    return patch,

#fonction qui permet de modifier la position 
def animate(k):
    patch.set_width(0.8)
    patch.set_height(0.5)
    patch.set_xy([x[k], y[k]]) #modification position
    patch.angle = yaw[k]        #modification angle



    N = 720
    alphainc=360/N
    #calcul zone safe 
    M=lidar(envir,position,orientation,N)
    MMMR=zonesafe(M,rv,m)
    orientation = 0
    i = 0
    while i<len(MMMR):
        #On trace ce que voit le lidar pour chaque point mesuré 

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
        thetap=atan((ylp)/(xlp))
        if xlp<0:
            thetap=pi+atan(ylp/xlp)
        thetacp=thetap+orientation*2*pi/360

        #calcul distance entre lidar et poit zone safe ref absolu 
        rp=sqrt(xlp**2+ylp**2)
        xlpc=rp*cos(thetacp)+x
        ylpc=rp*sin(thetacp)+y

        #on affiche le circuit
        envir=environment()
        n=len(envir)

        #y a plus qu'a afficher !
        plt.plot(xlc, ylc,"b:o")
        plt.plot(xlpc,ylpc,"r:o")
        i+=1
    



    return patch,

#on creer l'animation 
anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               frames=len(x),
                               interval=500,
                               blit=True)
"""
 1er argument - figure ou afficher 
 2e argument - fonction a executer
 3e argument - fonction initial a executer qui ajouter patch
 4e argument - [0,1,...,len(x) - 1] arguments succesives pris par animate
 5e argument - temps entre 2 positions 
 
 
 blit=True - optimisation du dessin 
 repeat=True - boucle par defaut peut etre mis a False
"""




plt.show()
