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

servo_pin = 18
moteur_pin=17
deg_0_pulse   = 0.5 
deg_180_pulse = 2.5
f = 50.0
period = 1000/f
k      = 100/period
deg_0_duty = deg_0_pulse*k
pulse_range = deg_180_pulse - deg_0_pulse
duty_range = pulse_range * k

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)
GPIO.setup(moteur_pin,GPIO.OUT)

pwm_servo = GPIO.PWM(servo_pin,f)
pwm_servo.start(0)

pwm_moteur = GPIO.PWM(moteur_pin,f)
pwm_moteur.start(2.5)

duty = deg_0_duty + (90/180.0)* duty_range

pwm_servo.ChangeDutyCycle(duty)
pwm_moteur.ChangeDutyCycle(0)


tours_init=50
limit_tour=1000000

lidar = RPLidar('/dev/ttyUSB0')
lidar.start_motor()
lidar.connect()

time.sleep(2)

data=[]
map=[1000 for i in range(360)]

angle_cible=0
angle_consigne=0
dmax=0

compteur=0
init=0

#vmin=1440
#vmax=1470
vmin=1440
vmax=1475
d=5000
        
window=curses.initscr()
window.nodelay(True)

go=0

try:

        for scan in lidar.iter_scans(500,10):
            key=window.getch()
            data.append(np.array(scan))
            X=data[-1]
            for j in range(len(X)):
                map[min(int(X[j][1])-1,359)]=X[j][2]
                
            mapt=traitement(map)
            if key==103:
                go=1
            if key==115:
                    curses.endwin()
                    lidar.stop_motor()
                    lidar.reset()
                    lidar.disconnect()
                    break
            #map=cone_obs(map)
            if go==1:
                
                v=vmin+(vmax-vmin)*(1-exp(-mapt[0]*3/d))
                #v=vmin+(vmax-vmin)*exp(-abs(angle_consigne-angle_cible)/30)
                
                
                consigne_moteur=v/200
                pwm_moteur.ChangeDutyCycle(consigne_moteur)
                
                dmax=0
                for i in range(-70,70):
                    if mapt[i]>dmax:
                        dmax=mapt[i]
                        angle_cible=i
                        
                print(angle_cible)
                print(map[angle_cible])
                
                angle_cible=evite_coins(angle_cible,200,map)
                
                #if angle_cible!=0:
                 #   angle_cible=angle_cible/abs(angle_cible)*22*(1-exp(-angle_cible**2/((v-vmin)/(vmax-vmin)*2000+600)))
                        #angle_cible=angle_cible/abs(angle_cible)*22*(1-exp(-angle_cible**2/800))
                
                if abs(angle_cible)<15:
                        angle_consigne=0
                elif abs(angle_cible)<50:
                        angle_consigne=min(10,max(-10,angle_cible))
                else:
                        angle_consigne=min(22,max(-22,angle_cible))
                
                
                consigne_servo=60*((angle_consigne+22)/44+1)

                duty = deg_0_duty + (consigne_servo/180.0)* duty_range
                pwm_servo.ChangeDutyCycle(duty)
                
                
                
                data=[]

    
except Exception as err:
        print(type(err).__name__)

        curses.endwin()
        lidar.stop_motor()
        lidar.reset()
        lidar.disconnect()
        


lidar.stop_motor()
lidar.reset()
lidar.disconnect()
