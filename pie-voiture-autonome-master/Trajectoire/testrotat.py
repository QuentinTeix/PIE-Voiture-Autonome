from math import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation

""" 
    ce code sert a simuler une voiture qui se deplace grace aux modules matplotlib.patches 
    et matplotlib.animation 
    
    Pour la voiture on créer un objet patches qui est un rectangle 
"""

#positions succesives de la voiture
x = [0,1,2]
y = [0,1,2]
#angle de la voiture 
yaw = [0.0, 45, 45]

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
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

#on creer le patch qui simule la voiture 
patch = patches.Rectangle((0, 0), 0, 0, fc='y')

#fonction d'initialisation qui affiche le patch sur la figure 
def init():
    ax.add_patch(patch)
    return patch,

#fonction qui permet de modifier la position 
def animate(i):
    patch.set_width(0.5)
    patch.set_height(0.8)
    patch.set_xy([x[i], y[i]]) #modification position
    patch.angle = yaw[i]        #modification angle
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
