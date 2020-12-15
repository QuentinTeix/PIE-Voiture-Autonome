

def environment():
    """
Cette fonction définit l'environnement virtuel de la course pour faire les tests, sont définis :
Le circuit intérieur et extérieur (les coordonnées des points données représentent les angles du circuit),
et quelques obstacles.
(le 1er point doit correspondre au dernier point visiblement)

Cela renvoie une liste des éléments de l'environnement.
    """
    circuitext=[[0,0],[9,0],[11,-2],[16,-2],[16,-10],[7,-10],[7,-6],[6,-5],[0,-5],[0,0]]
    circuitint=[[3,-2],[8,-2],[10,-4],[14,-4],[14,-7],[10,-7],[8,-5],[7,-4],[3,-4],[3,-2]]
    obst1=[[1.5,-2],[1.8,-2],[1.8,-2.3],[1.5,-2.3],[1.5,-2]]
    obst2=[[11,-8],[11.3,-8],[11.3,-8.3],[11,-8.3],[11,-8]]
    #obst3=[[13,-8],[13.3,-8],[13.3,-8.3],[13,-8.3],[13,-8]]

    envir=[circuitext,circuitint,obst1,obst2] #,obst3]
    return(envir)