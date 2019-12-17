import matplotlib.pyplot as plt
import math
import copy
import time
import triangulation
import sys
import numpy as np

class Graphe:
    def __init__(self,nom):
        self.sommets=[]
        self.aretes=[]
        self.nom=nom
        
    def ajouteSommet(self,x,y,couleur=(0.,0.,0.)):
        s=Sommet(x,y,1+len(self.sommets),couleur)
        self.sommets.append(s)
        return s #on retourne le sommet pour pouvoir par la suite le réutiliser
        
    def connecte(self,s1,s2,longueur,vitesse_moy,couleur=(0.,0.,0.)):
        a=Arete(s1,s2,longueur,vitesse_moy,couleur)
        s1.aretes.append(a)
        s2.aretes.append(a)
        self.aretes.append(a)
        return(a)
    
    def ajouteRoute (self, v1, v2, vmax, couleur=(0.,0.,0.)):
        self.connecte(v1,v2,v1.distance(v2),vmax,couleur)
        
    def ajouteNationale (self, v1, v2):
        self.connecte(v1,v2,v1.distance(v2),90,couleur = (1.,0.,0.))    

    def ajouteDepartementale  (self, v1, v2):
        self.connecte(v1,v2,v1.distance(v2),60,couleur = (1.,1.,0.))     

    def __str__(self):
        s="V("+ self.nom +") = { \n"
        for i in self.sommets:
            s+="\t"+"v"+str(i.indice)+" "+str(i)
        s+="} \n"
        s+="E("+ self.nom +") = { \n"
        for j in self.aretes:
            s+="\t {"+"v{},v{}".format(j.sommet1.indice,j.sommet2.indice)+"} "+str(j)
        s+="}"
        return s    
    def trace(self,afficheur):
        for a in self.aretes:
            afficheur.changeCouleur(a.couleur)
            afficheur.traceLigne((a.sommet1.x,a.sommet1.y),(a.sommet2.x,a.sommet2.y))
        for s in self.sommets:
            afficheur.changeCouleur(s.couleur)
            afficheur.tracePoint((s.x,s.y))
            afficheur.traceTexte((s.x,s.y),"v"+str(s.indice))
            if s.label != None:
                afficheur.traceTexte((s.x*1.1,s.y*1.1),str(s.label))

    def fixeCarburantCommeCout(self):
        for a in self.aretes :
            a.fixeCarburantCommeCout()
            
    def fixeTempsCommeCout(self):
        for a in self.aretes :
            a.fixeTempsCommeCout()
        
    def dijkstra(self,depart):
        for s in self.sommets:
            s.cumul = sys.float_info.max
            s.chemin = None
        depart.cumul=0
        L=[depart]
        while len(L)!=0:
            min_cumul=L[0].cumul
            indice_min=0
            for i in range(1,len(L)):
                if L[i].cumul<min_cumul:
                    min_cumul=L[i].cumul
                    indice_min=i
            s=L.pop(indice_min)
            for e in s.aretes:
                sp = e.voisin(s)
                raccourci = s.cumul+e.cout
                if raccourci < sp.cumul:
                    if sp.cumul==sys.float_info.max:
                        L.append(sp)
                    sp.chemin = e
                    sp.cumul = raccourci

    def traceArbreDesChemins(self):
        for s in self.sommets:
            if s.chemin is None:
                s.couleur=(0.,1.,0.)
            else:
                s.chemin.couleur=(0.,1.,0.)
    def cheminOptimal(self,arrivee):
        chemin_op=[]
        s=arrivee
        while s.chemin is not None:
            chemin_op.append(s.chemin)
            if s.chemin.sommet1 == s:
                s=s.chemin.sommet2
            else:
                s=s.chemin.sommet1
        chemin_op.reverse()
        return chemin_op
    
    def colorieChemin(self,chemin_a_colorier,c):
        for s in self.sommets:
            if s.chemin is None:
                s.couleur=(0.,1.,0.)
        s1 = chemin_a_colorier[-1].sommet1 
        s2 = chemin_a_colorier[-1].sommet2 
        S = [chemin_a_colorier[-2].sommet1,chemin_a_colorier[-2].sommet2]
        if s1 not in S :
            s1.couleur = (1.,0.,1.)
        else :
            s2.couleur = (1.,0.,1.)
        for a in chemin_a_colorier:
            a.couleur=c

    def matriceCout(self,tournee):
        n=len(tournee)
        C= np.zeros((n,n))
        for i in range(n):
            self.dijkstra(tournee[i])
            for j in range(i+1,n):
                C[i][j]=tournee[j].cumul
        C=C+np.transpose(C)
        return C

    def voyageurDeCommerceNaif(self,tournee):
        meilleurItineraire = []
        minCout = sys.float_info.max
        n=len(tournee)
        Nouvel_Itineraire=[0]
        cout = 0
        nonvisite = [True]*n
        M = self.matriceCout(tournee)
        
        def backtrack():
            # nonlocal déclare les variables comme étant celles définies dans la fonction englobante
            nonlocal minCout, meilleurItineraire,n, Nouvel_Itineraire, cout, M
            if len(Nouvel_Itineraire) == n :
                cout += M[Nouvel_Itineraire[-1],0]
                if cout < minCout :
                    minCout = cout
                    meilleurItineraire= [x for x in Nouvel_Itineraire]
                cout -= M[Nouvel_Itineraire[-1],0]
            else :
                for i in range(1,n) :
                    if nonvisite[i] :
                        cout += M[Nouvel_Itineraire[-1], i]
                        if cout+M[Nouvel_Itineraire[-1],0]<minCout:
                            Nouvel_Itineraire.append(i)
                            nonvisite[i] = False
                            backtrack()
                            Nouvel_Itineraire.pop()
                            nonvisite[i] = True
                        cout -= M[Nouvel_Itineraire[-1], i]
                                         
        backtrack ()
        meilleurItineraire =[tournee[i] for i in meilleurItineraire]

        return (minCout, meilleurItineraire)

    def traceItineraire(self,itineraire):
        for i in range(len(itineraire)):
            itineraire[i].label=i
            itineraire[i].couleur=(1.,0.5,0.2)
        
class Arete:
    def __init__(self,s1,s2,longueur,vitesse_moy,couleur=(0.,0.,0.)):
        self.longueur=longueur
        self.vitesse_moy=vitesse_moy
        self.sommet1=s1
        self.sommet2=s2
        self.couleur=couleur
        self.cout=1           # cout associé à l'arrête

    def voisin(self,s):
        if s == self.sommet1 :
            return self.sommet2
        else:
            return self.sommet1
        
    def __str__(self):
        return("(long. = "+str(self.longueur)+" km vlim. = "+str(self.vitesse_moy)+" km/h) \n")
    def fixeCarburantCommeCout(self):
        self.cout=self.longueur
        
    def fixeTempsCommeCout(self):
        self.cout=self.longueur/self.vitesse_moy

 
class Sommet:
    def __init__(self,x,y, ind,couleur=(0.,0.,0.)): #=None pour ne pas être obligé de renseigner l'attribut
        self.x=x
        self.y=y
        self.aretes=[]
        self.indice=ind
        self.couleur=couleur
        self.cumul=None #cout du chemin optimal pour aller du sommet de départ à ce sommet
        self.chemin=None #arrete parente dans le chemin optimal de d à ce sommet
        self.label=None #ordre de passage après avoir effectué l'algo du voyageur de commerce
        
    def milieu(self, s):
        return Sommet((self.x+s.x)*.5,(self.y+s.y)*.5,0)
    
    def distance_2 (self, v):
        return (self.x-v.x)**2 + (self.y - v.y)**2
    
    def distance (self, v):
        return math.sqrt (self.distance_2(v))
        
    def __str__(self):
        return("(x = "+str(self.x)+" km y = "+str(self.y)+" km) \n")
    
def gabriel(g):
    for idx,s1 in enumerate(g.sommets):
        for s2 in g.sommets[idx+1:]:
            M= s1.milieu(s2) 
            r_2=M.distance_2(s2)
            ne_contient_pas_de_point_dans_le_cercle=True
            for s in g.sommets:
                if s != s1 and s != s2:
                    if M.distance_2(s) <= r_2:
                        ne_contient_pas_de_point_dans_le_cercle=False
                        break
            if ne_contient_pas_de_point_dans_le_cercle:
                g.connecte(s1,s2,60,90)
    return g

def gvr(g):
    for s1 in g.sommets:
        for s2 in g.sommets:
            if s1==s2:
                continue
            d=s1.distance(s2)
            ne_contient_pas_de_point_dans_l_intersection=True
            for s in g.sommets:
                if s != s1 and s != s2:
                    if s1.distance(s) <= d and s2.distance(s) <= d:
                        ne_contient_pas_de_point_dans_l_intersection=False
                        break
            if ne_contient_pas_de_point_dans_l_intersection:
                g.connecte(s1,s2,60,90)
    return g

def reseau(g):
    graphe_gabriel=copy.deepcopy(g)
    gabriel(graphe_gabriel)
    graphe_gvr=copy.deepcopy(g)
    gvr(graphe_gvr)
    for arete in graphe_gabriel.aretes :
        g.ajouteDepartementale(arete.sommet1,arete.sommet2)
    for arete in graphe_gvr.aretes:
        if arete in g.aretes:
            continue
        else:
            g.ajouteNationale(arete.sommet1,arete.sommet2)
            

def reseau2 (g):
    for  i in range(len(g.sommets)):
        s1 = g.sommets[i]
        for j in range(i+1,len(g.sommets)):
            s2 = g.sommets[j]
            d=s1.distance(s2)
            M=Sommet((s2.x+s1.x)/2.0,(s2.y+s1.y)/2.0,0)
            ne_contient_pas_de_point_dans_le_cercle=True
            for s in g.sommets:
                if s != s1 and s != s2:
                    if M.distance(s) <= d/2:
                        ne_contient_pas_de_point_dans_le_cercle=False
                        break
            if ne_contient_pas_de_point_dans_le_cercle:           
                ne_contient_pas_de_point_dans_l_intersection=True
                for s in g.sommets:
                    if s != s1 and s != s2:
                        if s1.distance(s) <= d and s2.distance(s) <= d:
                            ne_contient_pas_de_point_dans_l_intersection=False
                            break
                if ne_contient_pas_de_point_dans_l_intersection:
                    g.ajouteNationale(s1,s2)
                else :
                    g.ajouteDepartementale(s1,s2)
    return g


                
def chronometre(fonctionTest, fonctionPreparation, parametres):

    temps = []
    # Pour chaque valeur de paramètre
    for p in parametres:
        # Génère les entrées du test pour la valeur p
        entrees = fonctionPreparation(p)
        # Lance le test pour ces entrées
        #print("t({}) = ".format(p), end="", flush=True)
        debut = time.time()
        fonctionTest(entrees)
        fin = time.time()
        # Mesure le temps d ' exécution
        t = (fin-debut)
        #print("{:.2f} s".format(t))
        temps.append(t)
        
    return temps



def delaunay(g):

    t = triangulation.Triangulation(g)

    # Définit une fonction destinée à être appelée
    # pour toute paire (s1,s2) de sommets
    # qui forme une arête dans la triangulation de Delaunay.
    # v3 et v4 sont les troisièmes sommets des deux triangles
    # ayant (s1,s2) comme côté.
    
    def selectionneAretes(graphe, v1, v2, v3, v4):
        # Fait de chaque arête de la triangulation
        # une nationale
        graphe.ajouteNationale(v1, v2)
        # Construit le graphe de retour, égal à la triangulation de Delaunay
    g = t.construitGrapheDeSortie(selectionneAretes)
    g.renomme("Delaunay("+ str(g.n()) + ")")
    return g

def complexite_dijkstra(g):
    g.dijkstra(g.sommets[0])
