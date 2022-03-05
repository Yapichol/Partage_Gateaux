#main

from Graphe import *

if __name__=="__main__":

    print("Debut")
    aleatoire = False
    
    #on test a vec un graphe que l'on crée
    if not aleatoire:
        g = Graphe()
        
        g.ajouter_noeud("A")
        g.ajouter_noeud("B")
        g.ajouter_liste_noeuds(["C","D","E"])
        
        g.ajouter_arc("A", "B")
        g.ajouter_arc("B", "A")
        g.ajouter_liste_arcs([("A","C"),("A","D"),("B","E")])

        #g.afficher_graphe()
        g.affiche()
        g.partage_aleatoire()
        g.afficher_graphe()
        stable,pas_stable= g.est_stable()
        print("Le graphe est stable? ",stable)
        print("Noeuds pas stables:",pas_stable)
        #print("\nDEVENIR STABLE")
        #g.devenir_stable(pas_stable)

        
    #on test avec un graphe généré aléatoirement
    else :
        
        g2 = Graphe()
        g2.generer_graphe(5,0.2)
        g2.afficher_graphe()
        g2.affiche()
        g2.partage_aleatoire()
        g2.afficher_graphe()
        stable,pas_stable= g2.est_stable()
        print("Le graphe est stable? ",stable)
        print("Noeuds pas stables:",pas_stable)
        
        
    print("Fin")