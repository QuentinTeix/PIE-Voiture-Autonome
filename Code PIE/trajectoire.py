import matplotlib.pyplot as plt
import numpy as np
import copy
from zonesafe import *
from adaptevitesserelat import *
from trouvecible import *
from environment import *
from environment2 import *
from lidar import *
from actualise import *
from actualise2 import *
from paramètres import *
from calculrayoncourbure import *
from math import *
from objectif import *




def trajectoire(P):
    #simulation de trajectoire:
    
    
    trajectoirex1=[]
    trajectoirey1=[]
    trajectoireor1=[]
    
    trajectoirex2=[]
    trajectoirey2=[]
    trajectoireor2=[]
    
    #initialisation
    

    [positioninit1,positioninit2,orientationinit1,orientationinit2,vinit1,vinit2,deltat,amaxlat,epsilonmax,amax,amin,tsb,l,larg,vmax,N,rv,m,alpha,lanti]=params()
    
    envir1=environment2(positioninit2,orientationinit2)
    envir2=environment2(positioninit1,orientationinit1)
    alphainc=360/N
    
    #intit de 1
    
    position1=positioninit1
    orientation1=orientationinit1
    v1=vinit1
    
    positionm11=positioninit1
    orientationm11=orientationinit1
    vm1=vinit1
    
    Mm11=lidar(envir1,positionm11,orientationm11,N)
    M1=lidar(envir1,position1,orientation1,N)
    
    MMMR1=zonesafe(M1,rv,m)
     
    MMMRC1=adaptevitesserelat (Mm11,M1,MMMR1,alpha,v1,deltat,lanti,orientation1,orientationm11)
    cible1=trouvecible(MMMRC1,v1)
    obj1=objectif(cible1,v1,deltat)
    R1=calculrayoncourbure(obj1)
    
    #init de 2
    
    position2=positioninit2
    orientation2=orientationinit2
    v2=vinit2
    positionm12=positioninit2
    orientationm12=orientationinit2
    vm2=vinit2 
    
    Mm12=lidar(envir2,positionm12,orientationm12,N)
    M2=lidar(envir2,position2,orientation2,N)
    
    MMMR2=zonesafe(M2,rv,m)
    
    MMMRC2=adaptevitesserelat (Mm12,M2,MMMR2,alpha,v2,deltat,lanti,orientation2,orientationm12)
    
    cible2=trouvecible(MMMRC2)
    obj2=objectif(cible2,v2,deltat)
    R2=calculrayoncourbure(obj2)
    
    
    
    #nombre de pts de la traj à tracer
    j=0
    
    while j<P:
        
        
        trajectoirex1.append(position1[0])
        trajectoirey1.append(position1[1])
        trajectoireor1.append(orientation1)
        
        trajectoirex2.append(position2[0])
        trajectoirey2.append(position2[1])
        trajectoireor2.append(orientation2)
        
        #mise à jour des variables 1
        positionm11=copy.deepcopy(position1)
        orientationm11=copy.deepcopy(orientation1)
        vm11=copy.deepcopy(v1)
        
        [position1,orientation1,v1]=actualise2(R1,v1,position1,obj1,cible1,orientation1,deltat,amaxlat,epsilonmax,amax,amin,tsb,l,vmax,N)
       
        Mm11=lidar(envir1,positionm11,orientationm11,N)
        envir1=environment2(position2,orientation2)
        M1=lidar(envir1,position1,orientation1,N)
        MMMR1=zonesafe(M1,rv,m)
        MMMRC1=adaptevitesserelat (Mm11,M1,MMMR1,alpha,v1,deltat,lanti,orientation1,orientationm11)
        cible1=trouvecible(MMMRC1)
        obj1=objectif(cible1,v1,deltat)
        R1=calculrayoncourbure(obj1)
        
        #mise à jour des variables 2
        positionm12=copy.deepcopy(position2)
        orientationm12=copy.deepcopy(orientation2)
        vm12=copy.deepcopy(v2)
        
        [position2,orientation2,v2]=actualise2arc(R2,v2,position2,obj2,cible2,orientation2,deltat,amaxlat,epsilonmax,amax,amin,tsb,l,vmax,N)
       
        Mm12=lidar(envir2,positionm12,orientationm12,N)
        envir2=environment2(position1,orientation1)
        M2=lidar(envir2,position2,orientation2,N)
        MMMR2=zonesafe(M2,rv,m)
        MMMRC2=adaptevitesserelat (Mm12,M2,MMMR2,alpha,v2,deltat,lanti,orientation2,orientationm12)
        cible2=trouvecible(MMMRC2)
        obj2=objectif(cible2,v2,deltat)
        R2=calculrayoncourbure(obj2)
        
        #préparation de cible pour affichage 
        #xcible=cible1[0]  
        #ycible=cible1[1]
        #=atan((ycible)/(xcible))
        #if xcible<0:
        #    thetacible=pi+atan(ycible/xcible) 
        #thetaciblec=thetacible+orientation1*2*pi/360
        #rcible=sqrt(xcible**2+ycible**2)
        #xciblec=rcible*cos(thetaciblec)+position1[0]
        #yciblec=rcible*sin(thetaciblec)+position1[1]
    
        
        
        
        #debugage
    
        print(j)
        #print('vitesse',v)
        #print('orientation', orientation)
        #print('R',R)
        #if j%50==0:
        #    print(j)
        
        
        
        
        j+=1
        
    return([[trajectoirex1,trajectoirey1,trajectoireor1],[trajectoirex2,trajectoirey2,trajectoireor2]])
