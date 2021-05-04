'''
Fonction qui permet d'arrêter le lidar de manière manuelle
'''
from rplidar import RPLidar
lidar = RPLidar('/dev/ttyUSB0')
lidar.stop_motor()
lidar.reset()
lidar.disconnect()
