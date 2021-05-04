import numpy as np
import copy
from zonesafe import *
from adaptevitesserelat import *
from trouvecible import *
from environment import *
from lidar import *
from calculrayoncourbure import *
from math import *
from rplidar import RPLidar
from evite_murs import *
from traitement import *
from cone_obs import *
import time

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
pwm_moteur.ChangeDutyCycle(8)


tours_init=50
limit_tour=1000000

lidar = RPLidar('/dev/ttyUSB0')
lidar.start_motor()
lidar.connect()

time.sleep(2)

data=[]
map=[[i,1000] for i in range(360)]

angle=0
dmax=0

compteur=0
init=0
for scan in lidar.iter_scans(500,10):
    compteur+=1
    data.append(np.array(scan))
    X=data[-1]
    for j in range(len(X)):
        map[min(int(X[j][1])-1,359)][1]=X[j][2]
        #map[int(X[j][1])-1][1]=X[j][2]
    map=traitement(map)
    #print(map)
    #map=cone_obs(map)
    if compteur>tours_init+1:
        dmax=0
        for i in range(-90,90):
            if map[i][1]>dmax:
                dmax=map[i][1]
                angle=i
                
        print(angle)
        print(map[angle][1])
        
        angle=evite_coins(angle,15,200,map)
        
        if angle!=0:
            angle_consigne=angle/abs(angle)*25*(1-exp(-angle*angle/800))
            
        
        consigne=60*((angle_consigne+25)/50+1)

        duty = deg_0_duty + (consigne/180.0)* duty_range
        pwm_servo.ChangeDutyCycle(duty)
        data=[]
        if compteur>limit_tour:
            break

lidar.stop_motor()
lidar.reset()
lidar.disconnect()
