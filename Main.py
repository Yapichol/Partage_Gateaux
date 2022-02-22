#main

from Graphe import *

if __name__=="__main__":

    print("Debut")
    g = Graphe()
    g.ajouter_noeud("A")
    g.ajouter_noeud("B")
    g.ajouter_arc("A", "B")
    g.ajouter_arc("B", "A")
    g.ajouter_arc("A", "A")
    g.afficher_graphe()
    
    print("Fin")
