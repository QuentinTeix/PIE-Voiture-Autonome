from math import *
from intersection import *
import matplotlib.pyplot as plt

def trouvecible (environment_adapte):
    """
    Cette fonction sert a trouver une cible otpimale, pour cela on calcule la zone safe puis on cherche le point de cette zone 
    qui est le plus eloigné de la position actuelle et qui ne coupe auncun segment 
    
    environment_adapte --> MMRC  [(thetai,ri,xi,yi,xpi ou xpiprim,ypi ou ypiprim)]
    environment_adapte_2 --> MMRCT[(thetai,ri,xi,yi,xpi ou xpprimi,ypi ou ypprimi,rpi)] trié par rpi croissant
    segments=[(xpprimi,ypprimi,xpprimip1,ypprimip1)]  --> CA SERT A RIEN NON ? SI UN POINT COUPE UN SEGMENT ON NE POURAIT PAS LE VOIR ... 
    
    """
    
    environment_adapte_2=[]
    NNN=len(environment_adapte)
    i=0 
    
    #on créer environment_adapte_2 en ajoutant les distance entre le point de la zone safe et le lidar 
    while i<NNN:
        d=environment_adapte[i][4]**2+environment_adapte[i][5]**2
        liste=environment_adapte[i]+[d]
        environment_adapte_2.append(liste)
        i+=1
    # on trie par ordre decroissant selon la distance (on veut le point le plus loin ! )
    environment_adapte_2.sort(key=lambda x: x[6])
    environment_adapte_2.reverse()
    
    
    
    #partie avec segment on calcul segment entre point mesure lidar et on verifie qu'on ne les coupe pas 
    segments=[]
    i=0
    while i<(NNN-1):
        segments.append([environment_adapte[i][4],environment_adapte[i][5],environment_adapte[i+1][4],environment_adapte[i+1][5]])
        
        #plt.plot([environment_adapte[i][4]+4,environment_adapte[i+1][4]+4],[environment_adapte[i][5]-1,environment_adapte[i+1][5]-1],"y-+") #debugage
        i=i+1
        
    i=0
    while i<NNN:
        xpi=environment_adapte_2[i][4]
        ypi=environment_adapte_2[i][5]
        j=0
        while j<len(segments) and intersection((xpi,ypi),segments[j])!=1:
            j+=1
        if j==len(segments): #alors le pt pi trouvé une cible qui ne coupe aucun segment"
            return(environment_adapte_2[i])
        i+=1
    #-------------------------------------------------------------------------------------------------------------------
    print('ERREUR pas de cible optimale')
    return('ERREUR')
     
