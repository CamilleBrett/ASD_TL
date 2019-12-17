# Modélisation du problème du voyageur de commerce

Ce projet réunit différents scripts avec le but de présenter le problème du voyageur de commerce. Il a été créé dans le cadre du cours Algorithmes et Structures de Données.

## Le problème du voyageur de commerce

On considère un marchand qui doit visiter ses clients dans n villes distinctes en parcourant le moins de kilomètres possible, avant de rentrer chez lui. Il faut donc trouver sur la carte le circuit le plus court parmis tous les circuits de la carte passant par la ville de résidence du marchand et les n villes de ses clients.

## Le fichier graphe
 Le fichier `graphe.py` génère une structure de données de type graphe représentant le réseau routier sur lequel le voyageur se déplace. Les routes peuvent être des départementales ou des nationales (le voyageur ira plus ou moins vite sur ces routes).

 * Les fonctions `gabriel` et `gvr` génèrent respectivement des graphes de Gabriel et de voisinage relatif (GVR) à partir du nuage de points g reçu en argument.

 * La fonction `reseau` génère un réseau routier à partir du nuage de points g reçu en argument. Les nationales correspondent aux arêtes du GVR et les départementales sont les arêtes du graphe de Gabriel.

 * La fonction `delaunay`génère une triangulation de Delaunay à partir d'un nuage de points g.

* La fonction `reseau2` génère un réseau routier de manière plus efficace que la fonction `reseau`, en utilisant la triangulation de Delaunay.

* La méthode `dijkstra` effectue l'algorithme de Djikstra dans le but de trouver le chemin le plus court.

* La méthode `traceArbreDesChemins` colore les arêtes appartenant aux chemins optimaux afin que les résultats de Dijkstra soit visible.

* On suppose que chaque ville à visiter par le voyageur est désignée par un indice entre 1 et n et la ville de départ par l'indice 0. La matrice de coût est définie comme une matrice C de taille (n+1).(n+1) telle que chaque coefficient C(i,j) vaut le coût du trajet optimal pour aller de la ville i à la ville j. La méthode `matriceCout` calcule cette matrice.

* La méthode `voyageurDeCommerceNaif` resout le problème comme un problème de backtracking.

## Le fichier test 

Ce fichier permet de vérifier le bon fonctionnement des fonctions définies précédemment.