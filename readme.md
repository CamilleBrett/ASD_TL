# Modélisation du problème du voyageur de commerce

Ce projet réunit différents scripts avec le but de présenter le problème du voyageur de commerce. Il a été créé dans le cadre du cours Algorithmes et Structures de Données.

## Le fichier graphe
 Le fichier `graphe.py` génère une structure de données de type graphe représentant le réseau routier sur lequel le voyageur se déplace. Les routes peuvent être des départementales ou des nationales (le voyageur ira plus ou moins vite sur ces routes).

 * Les fonctions `gabriel` et `gvr` génèrent respectivement des graphes de Gabriel et de voisinage relatif (GVR) à partir du nuage de points g reçu en argument.

 * La fonction `reseau` génère un réseau routier à partir du nuage de points g reçu en argument. Les nationales correspondent aux arêtes du GVR et les départementales sont les arêtes du graphe de Gabriel.

 * La fonction `delaunay`génère une triangulation de Delaunay à partir d'un nuage de points g.

* La fonction `reseau2` génère un réseau routier de manière plus efficace que la fonction `reseau`, en utilisant la triangulation de Delaunay.

* La méthode `dijkstra` effectue l'algorithme de Djikstra dans le but de trouver le chemin le plus court.



