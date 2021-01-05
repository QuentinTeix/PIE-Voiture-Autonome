# Code du PIE Voiture autonome


## Ce que fait le code (globalement)

(à compléter...)


## Méthodologie de trajectoire

Il faut qu'on se mette d'accords sur la méthode générale de conduite de la voiture

- Est-ce que l'on garde la méthode de l'année dernière, ou est-ce que l'on en prend une autre ?
(https://tel.archives-ouvertes.fr/tel-01160233/document)


- Cartographie de la piste pendant les 2 tours d'essais ? Pour ne se concentrer que sur les adversaires pendants la courses
- Calcul de trajectoire courbe directement ? Cela prend les adversaires en compte ?



## Ce qu'il reste à faire:

- Faire un rapport sur ce qui a été compris du code
- Terminer de commenter et de comprendre les fonctions du code de l'année dernière.
- Coder les fonctions manquantes selon la méthode suivie.



Description du code :


- trajectoire.py

module final qui calcul la trajectoire 
Methode de direction de la voiture : 
	1- On prend les mesures du LIDAR
	2- on determine la zone safe 
	3- On adapte la zone safe a la vitesse relative 
	4- on trouve la cible 
	5- on en deduit le rayon de braquage des roues 


- zonesafe.py

module qui calcul la zone safe dans laquelle il ne faut pas aller 

- testrotat.py

Modelisation de la voiture a l'aide d'un patch 
a ete repris dans la modelisation dynamique de la voiture 

- vsimulationavecvuelidar.py

Module de modelisation de la trajectoire mais marche pas j'ai recodé ce module dans 
vsimulationavecvuelidar_new.py afin d'avoir une modelisation dynamique 

- vsimulationavecvuelidar_new.py

Module qui permet de visualiser l'avancement de la voiture dans l'environement Pour l'instant les positions succesives ont ete rentrées a la main mais l'objectif a terme est de les faires calculer directement a l'lalgorithme afin de verifier que la simulation marche 
