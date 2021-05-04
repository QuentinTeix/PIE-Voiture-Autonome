import time
import RPi.GPIO as GPIO

moteur_pin=17

GPIO.setmode(GPIO.BCM)
GPIO.setup(moteur_pin,GPIO.OUT)

pwm_moteur = GPIO.PWM(moteur_pin,50)
pwm_moteur.start(2.5)

pwm_moteur.ChangeDutyCycle(0)
time.sleep(2)
pwm_moteur.ChangeDutyCycle(10)
time.sleep(2)

for i in range(0,100):
	pwm_moteur.ChangeDutyCycle(i*0.1)
	time.sleep(0.1)

pwm_moteur.ChangeDutyCycle(0)
