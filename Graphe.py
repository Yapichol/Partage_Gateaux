#graph

class Graphe :

    def __init__(self) :
        self.noeuds = []
        self.arcs = []

    def afficher_graphe(self):
        print("Liste des noeuds : ", self.noeuds)
        print("Liste des arcs : ", self.arcs)

    def ajouter_noeud(self, nom):
        pres = False
        for i in self.noeuds:
            if i[0] == nom :
                pres = True
        if not pres :
            self.noeuds.append((nom, 0))
        else :
            print("Le noeud ", nom, " existe deja !")

    def ajouter_arc(self, noeud1, noeud2):
        n1 = False
        n2 = False
        for i in self.noeuds:
            if i[0] == noeud1 :
                n1 = True
            if i[0] == noeud2 :
                n2 = True    
        if noeud1 != noeud2 and n1 and n2 and ((not ((noeud1, noeud2) in self.arcs)) and (not ((noeud2, noeud1) in self.arcs))):
            self.arcs.append((noeud1, noeud2))
        else :
            print("Erreur au niveau des noeuds ou arcs")
