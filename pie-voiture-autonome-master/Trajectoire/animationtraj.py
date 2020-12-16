"""
Ce code permet d'afficher une petite animation d'un cube sur un cadrillage qui tourne en avançant (5 images seulement)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation

# Le nombre d'arguments donne le nombre d'images
x = [0, 1, 2, 3, 4]
y = [0, 1, 2, 3, 4]
yaw = [0, 0.5, 1.3, 2.1, 2.9]

# Initialisation de la figure
fig = plt.figure()
plt.axis('equal')
plt.grid()
ax = fig.add_subplot(111)
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

patch = patches.Rectangle((0, 0), 0, 0, fc='y')

def init():
    ax.add_patch(patch)
    return patch,

def animate(i):
    patch.set_width(1.0)
    patch.set_height(1.0)
    patch.set_xy([x[i], y[i]])
    patch.angle = -np.rad2deg(yaw[i])
    return patch,

anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               frames=len(x),
                               interval=500,            #interval de temps entre les images de l'animation
                               blit=True)
plt.show()