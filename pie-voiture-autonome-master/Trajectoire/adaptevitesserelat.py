from math import *
import copy

"""
ancienne notations:
M = coord_lidar
environement = environment
N = len_coord_lidar
NNN = len_env
"""


def adaptevitesserelat (coord_lidar_prec,coord_lidar,environement,alpha,v,deltat,rmax,orientation,orientationm1):
    
    """
    Cette fonction déplace la zone de sécurité près du bord en fonction de la vitesse du véhicule par rapport au bord.
    
    IMPORTANT 
        corrige cone entre -alpha et alpha 
        reste inchangé sinon 

    coord_lidar_prec = [(thetai,ri)] -> liste des tuples de coordonnées du lidar au temps t-dt
    coord_lidar = [(thetai,ri)] liste des tuples de coordonnées lidar
    environment = [(thetai,ri,xi,yi,xpi,ypi)] (voir zonesafe.py)
    environment_pi_cone = [(thetai,ri,xi,yi,xpi,ypi)] ou pi est tq le vecteur pipti est orthogonal au bord du circuit et de norme rv+m des pi entre -alpha et alpha
    deltat -> intervalle de temps entre deux mesures lidar (paramètres)
    environment_corr = [(thetai,ri,xi,yi,xpi,ypi,xpprimi,ypprimi)] environement corrigé
        où pprim est le point pi repositionné en foncion de sa vitesse relative (vrai que pour les pi dans le cone alpla -alpha les autres sont inchangés)
    environment_corr_2 = [(thetai,ri,xi,yi,xpi ou xpprimi,ypi ou ypprimi)] -> environment corrigé final (INCOMPREHENSIBLE)
    """


    environment_pi_cone=[]
    environment_corr=[]
    environment_corr_2=copy.deepcopy(environement)
    len_env=len(environement)
    i=0
    len_coord_lidar=len(coord_lidar)

    # on ne garde les coordonnées que quand on est dans un cone
    while i<len_env:
        if (environement[i][0]*360/len_coord_lidar)<alpha:
            environment_pi_cone.append(environement[i])
        i+=1
    i=0
    while i<len_env:   #création du environment_pi_cone
        if (environement[i][0]*360/len_coord_lidar)>(360-alpha):
            environment_pi_cone.append(environement[i])
        i+=1
    i=0
    nnn=len(environment_pi_cone)

    while i<nnn:

        theta = int(environment_pi_cone[i][0])
        # 'coord_lidar' louche ensuite, plutôt 'environment' ??
        vrel = (coord_lidar[theta][1]-coord_lidar_prec[(theta + int((orientation-orientationm1)/360*len_coord_lidar))%len_coord_lidar][1])/deltat
        # approximation de la dérivée de la distance à l'objet par rapport au temps"
        # ATTENTION REMPLACER (orientation-orientationm1) par les données de l'accéléromètre dorientation/dt*deltat
        # orientation et orientationm1 vallent 0 pour le moment

        thetap = atan(environment_pi_cone[i][5]/environment_pi_cone[i][4]) # angle de coordonnées polaires du point p, attention c'est bien en angle cette fois
        rp = sqrt(environment_pi_cone[i][5]**2+environment_pi_cone[i][4]**2) # rayon de coordonnées polaires du point p

        if vrel<0:
            rpprim=min(rp*v*cos(thetap)/(-vrel),rmax) #adaptation du rayon en fonction de la vitesse relative à la voituredu point qu'il désigne"
            #on pourrait modifier le ryon en prenant aussi compte de l'accélération relative!
        if vrel>=0:
            rpprim=rmax
        xpprim=rpprim*cos(thetap)
        ypprim=rpprim*sin(thetap)
            
        
            
        environment_corr.append((environment_pi_cone[i]+[xpprim,ypprim]))
        i+=1
    i=0
    
    #bon courrage pour comprendre ca 
    while i<len(environment_corr):
        j=0
        while j<len_env:
            if environment_corr[i][0]==environment_corr_2[j][0]:
                environment_corr_2[j][4]=environment_corr[i][6]
                environment_corr_2[j][5]=environment_corr[i][7]
            j+=1
        i+=1
    
    return(environment_corr_2)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
        