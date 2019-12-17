import graphe
import graphique
import random
import copy
import matplotlib.pyplot as plt

def creerGrapheFigure1():
    "Crée le Graphe de la figure 1"
    g = graphe.Graphe("Graphe de la figure 1")
    s1 = g.ajouteSommet(1.0, 1.0)
    s2 = g.ajouteSommet(2.0, 3.5)
    s3 = g.ajouteSommet(2.5, 2.5)
    s4 = g.ajouteSommet(5.0, 2.0)
    g.connecte(s1, s2, 4.0, 90.)
    g.connecte(s1, s4, 5.2, 124.)
    g.connecte(s2, s3, 2.0, 54.)
    g.connecte(s2, s4, 5.0, 90.)
    return g

def testQuestion1_2():
    '''Teste que la création d'un graphe ne plante pas '''
    print("Question 1.2 :")
    creerGrapheFigure1()
    print("Ok. Pas de plantage")  

def testQuestion1_3(): 
    ''' Teste l'affichage d'un graphe dans la console '''
    print("Question 1.3 :")
    g = creerGrapheFigure1()
    print(g)
    
def testQuestion1_4(): 
    ''' Teste l'affichage graphique d'un graphe identique à celui de la figure 1.b) '''
    graphique.affiche(creerGrapheFigure1(),(3.,2.),100.)

def testQuestion1_5():
    ''' Teste l'affichage graphique d'un graphe identique à celui de la figure 1.ben couleur '''

    g = graphe.Graphe("Graphe de la figure 1 colorée")
    s1 = g.ajouteSommet(1.0, 1.0,(1.,0.,1.))
    s2 = g.ajouteSommet(2.0, 3.5,(0.,1.,0.))
    s3 = g.ajouteSommet(2.5, 2.5,(0.,0.,1.))
    s4 = g.ajouteSommet(5.0, 2.0,(0.,1.,1.))
    g.connecte(s1, s2, 4.0, 90.,(1.,1.,0.))
    g.connecte(s1, s4, 5.2, 124.,(1.,0.,0.))
    g.connecte(s2, s3, 2.0, 54.,(1.,1.,0.))
    g.connecte(s2, s4, 5.0, 90.,(1.,0.,0.))
    graphique.affiche(g,(3.,2.),100.)

def pointsAleatoires(n,L):
    '''
    Retourne un graphe sans arretes, constitue
    de n sommets positionnes aleatoirement dans
    un carre de cote L
    '''
    g = graphe.Graphe("Graphe de la figure 2")
    for i in range(n):
        x=random.random()*(L+1)-L*.5
        y=random.random()*(L+1)-L*.5
        g.ajouteSommet(float(x),float(y))
    return g

def testQuestion2_2():
    '''On verifie le bon fonctionnement de la methode pointsAleatoires'''
    g= pointsAleatoires(10,20)
    graphique.affiche(g,(3.,2.),100.)

def testQuestion2_3():
    '''
    On verifie le bon fonctionnement des methodes
    ajouteNationale, ajouteDepartementale, ajouteRoute.
    '''
    g = pointsAleatoires(10,20)
    g.ajouteNationale(g.sommets[0], g.sommets[1])
    g.ajouteDepartementale(g.sommets[2], g.sommets[3])
    g.ajouteRoute(g.sommets[4],g.sommets[5],50.,(0.,1.,0.))
    graphique.affiche(g,(3.,2.),1000.)
                  

def testQuestion2_4():
    '''On verifie le bon fonctionnement de la methode gabriel'''
    g = pointsAleatoires(10,20)
    graphe_gabriel=graphe.gabriel(g)
    graphique.affiche(g,(3.,2.),100.)

def testQuestion2_5():
    '''On verifie le fonctionnement de la fonction reseau'''
    g = pointsAleatoires(100,20)
    graphe.reseau(g)
    graphique.affiche(g,(3.,2.),100.)

def testQuestion2_6():
    '''On mesure le temps necessaire a la construction d'un reseau routier'''
    parametres = [ 2**x  for x in range(0,10)]
    def prepare(n):
        return pointsAleatoires(n,100)
    plt.loglog (parametres, graphe.chronometre(graphe.reseau2, prepare, parametres),'b')          
    plt.show()

def testQuestion3_1():
    '''
    On verifie que les chemins optimaux determines par
    la methode dijkstra forment un arbre.
    '''
    g = pointsAleatoires(100,20)
    graphe_gabriel=graphe.gabriel(g)
    graphe_gabriel.dijkstra(graphe_gabriel.sommets[0])
    graphe_gabriel.traceArbreDesChemins()
    graphique.affiche(graphe_gabriel,(3.,2.),1000.)

def testQuestion3_2():
    '''
    On compare les resultats de dijkstra sur deux memes reseaux routiers,
    l'un ayant le carburant comme cout et l'autre le temps.
    '''
    g_carb = pointsAleatoires(100,200)
    graphe.reseau2(g_carb)
    g_temps=copy.deepcopy(g_carb)
    for a in g_carb.aretes:
        a.fixeCarburantCommeCout()
    g_carb.dijkstra(g_carb.sommets[0])
    g_carb.traceArbreDesChemins()
    graphique.affiche(g_carb,(3.,2.),100.,blocage=False)
    for a in g_temps.aretes:
        a.fixeTempsCommeCout()
    g_temps.dijkstra(g_temps.sommets[0])
    g_temps.traceArbreDesChemins()
    graphique.affiche(g_temps,(3.,2.),100.)

def testQuestion3_3():
    '''On mesure le temps de calcul de l'algorithme Dijkstra'''
    parametres = range(3,100)
    def prepare(n):
        return (graphe.reseau2(pointsAleatoires(n,150)))
    plt.loglog (graphe.chronometre(graphe.complexite_dijkstra, prepare, parametres),parametres,'b')  
    plt.show()

def testQuestion3_4():
    '''On affiche un graphe ou le chemin optimal est colore'''
    g = pointsAleatoires(100,100)
    gtest=graphe.reseau2(g)
    gtest.fixeCarburantCommeCout()
    gtest.dijkstra(gtest.sommets[0])
    arrivee=gtest.sommets[60]
    chemin_opti=gtest.cheminOptimal(arrivee)
    gtest.colorieChemin(chemin_opti,(1.,0.,1.))
    graphique.affiche(gtest,(3.,2.),100.)                   

def testQuestion4_1():
    '''On teste le fonctionnement de matriceCout'''
    g = pointsAleatoires(100,100)
    gtest=graphe.reseau2(g)
    tournee=[gtest.sommets[int(random.random()*100)] for i in range(6)]
    res=gtest.matriceCout(tournee)
    print(res)
    afficher=input("Appuyer sur v pour afficher le graphe : ")  #pour afficher la matrice de cout avant le graphe
    if afficher=="v":
        graphique.affiche(gtest,(3.,2.),100.)

def testQuestion4_2():
    '''On verifie la resolution du probleme'''
    g = pointsAleatoires(20,200)
    gtest=graphe.reseau2(g)
    tournee=gtest.sommets[0:6]
    (cout,itineraire)=gtest.voyageurDeCommerceNaif(tournee)
    gtest.traceItineraire(itineraire)
    graphique.affiche(gtest,(3.,2.),200.)

def testQuestion4_3():
    '''On evalue le temps de calcul en fonction du nombre de villes a visiter.'''
    g = pointsAleatoires(100,200)
    gtest=graphe.reseau2(g)
    parametres = range(3,15)
    def prepare(n):
        return [gtest.sommets[int(random.random()*100)] for i in range(1,n+1)]
    plt.plot(parametres,graphe.chronometre(gtest.voyageurDeCommerceNaif, prepare, parametres),'b')  
    plt.show()

if __name__ == "__main__":
    #testQuestion1_2()
    #testQuestion1_3()
    #testQuestion2_4()
    #testQuestion3_1()
     testQuestion4_3()
