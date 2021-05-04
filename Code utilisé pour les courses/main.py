'''
Ce programme est celui qui a été utilisé et finalisé pendant les courses de voitures à l'ENS.
Il est à utiliser APRES QUE LES MOTEURS AIENT ETE INITIALISES via le programme "init_moteur.py"
De même, il faudra utiliser 
Il se décompose en 3 parties principales:


I. Importation des modules et des fonction extérieures.

II. Initialisation du code.
        1. Définition des constantes
        2. Initialisation des différents moteurs
        3. Initialisation du lidar
        4. Initialisation des variables pour la première boucle
        5. Initialisation de la fenêtre spéciale

III. Boucle principale.
        1. Traitement de la vision de l'environnement
        2. Choix de comportement de la voiture
        3. Conduite de la voiture
                3.1 Réglage de la vitesse de conduite
                3.2 Réduction du champ de vision
                3.3 Réglage de l'angle de braquage

'''

############################################################
## I. Importations des modules et fonctions extérieures ####
############################################################
import numpy as np
import copy
from math import *
from rplidar import RPLidar
from evite_murs import *
from traitement import *
from cone_obs import *
import time
import curses
import RPi.GPIO as GPIO


#####################################
#### II. Initialisation du code #####
#####################################

######## Définition des constantes ##########
servo_pin = 18
moteur_pin = 17
deg_0_pulse = 0.5 
deg_180_pulse = 2.5
f = 50.0
period = 1000/f
k      = 100/period
deg_0_duty = deg_0_pulse*k
pulse_range = deg_180_pulse - deg_0_pulse
duty_range = pulse_range * k
duty = deg_0_duty + (90/180.0)* duty_range
tours_init = 50
limit_tour = 1000000


###### Initialisation des différents moteurs ######
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)
GPIO.setup(moteur_pin,GPIO.OUT)

pwm_servo = GPIO.PWM(servo_pin,f)
pwm_servo.start(0)
pwm_moteur = GPIO.PWM(moteur_pin,f)
pwm_moteur.start(2.5)
pwm_servo.ChangeDutyCycle(duty)
pwm_moteur.ChangeDutyCycle(0)

#### Initialisation du lidar ############
lidar = RPLidar('/dev/ttyUSB0')
lidar.start_motor()
lidar.connect()

time.sleep(2)   # Petit temps mort de sécurité


#### Initialisation des variables pour la première boucle #####
data = []
map = [1000 for i in range(360)]
angle_cible = 0
angle_consigne = 0
dmax = 0
compteur = 0
init = 0

#vmin=1440      # valeurs qui dépendent beaucoup de la batterie utilisée
#vmax=1470
vmin=1440
vmax=1475
d=5000
go = 0

# Initialisation de la fenêtre spéciale (Qui permet de donner des directives à la voiture pendant que le programme tourne).
window=curses.initscr()
window.nodelay(True)


######################################
### III. Boucle principale ###########
######################################
try:
        ########### 1. Traitement de la vision de l'environnement ##########
        for scan in lidar.iter_scans(500,10):
            key = window.getch()          # A chaque itération on récupère les commandes données par l'utilisateur (s'il y en a)
            data.append(np.array(scan))
            X=data[-1]

            '''
            Mise en forme de la map s2. Choix de comportement de la voitureous forme plus compréhensible:
            (on a alors le format "map[angle] = distance" selon les données lidar)
            '''
            for j in range(len(X)):
                map[min(int(X[j][1])-1,359)]=X[j][2]

            mapt = traitement(map)      # Lissage du bruit, voir "traitement.py"

        ###########  ##########
            if key == 103:        # Touche appuyée = 'g' --> faire partir la voiture
                go = 1
            if key == 115:        # Touche appuyée = 's' --> faire arrêter la voiture
                    curses.endwin()
                    # Arrêt du lidar
                    lidar.stop_motor()
                    lidar.reset()
                    lidar.disconnect()
                    break
        
        ########### 3. Conduite de la voiture ##########
            if go == 1:
                ##### 3.1 Réglage de la vitesse de conduite #####
                consigne_moteur = (1/200)*( vmin+(vmax-vmin)*(1-exp(-mapt[0]*3/d)) ) # Règle la vitesse des moteurs selon la distance au mur d'en face
                pwm_moteur.ChangeDutyCycle(consigne_moteur)
                
                ##### 3.2 Réduction du champ de vision #####
                dmax=0
                for i in range(-70,70):         # la voiture ne regarde que dans ce cône pour se diriger
                    if mapt[i]>dmax:            # On cherche la distance au mur la plus grande
                        dmax=mapt[i]
                        angle_cible=i

                ## Affichage de vérification       
                print(angle_cible)
                print(map[angle_cible])
                
                angle_cible = evite_coins(angle_cible,200,map)          # Voir "evite_murs.py"

                ##### 3.3 Réglage de l'angle de braquage #####
                if abs(angle_cible) < 15:         # Aller tout droit
                        angle_consigne = 0
                elif abs(angle_cible) < 50:       # Tourner pas trop fort
                        angle_consigne=min(10,max(-10,angle_cible))
                else:                             # Tourner à fond
                        angle_consigne=min(22,max(-22,angle_cible))
                
                
                consigne_servo=60*((angle_consigne+22)/44+1)            # Conversion en puissance de servo-moteur
                duty = deg_0_duty + (consigne_servo/180.0)* duty_range
                pwm_servo.ChangeDutyCycle(duty)
                
                # Vide du cache
                data=[]
    
except Exception as err:        # Gestion des erreurs ou interruption du code
        print(type(err).__name__)
        curses.endwin()
        lidar.stop_motor()
        lidar.reset()
        lidar.disconnect()

## arrêt du lidar
lidar.stop_motor()
lidar.reset()
lidar.disconnect()