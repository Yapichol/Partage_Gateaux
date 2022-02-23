#graph
import networkx as nx
import random

class Graphe :

    def __init__(self) :
        self.noeuds = []
        self.arcs = []

    def afficher_graphe(self):
        """Affiche les listes correspondant aux noeuds et aux arcs du graphe"""
        print("Liste des noeuds : ", self.noeuds)
        print("Liste des arcs : ", self.arcs)

    def ajouter_noeud(self, nom):
        """Ajoute un noeud au graphe si celui-ci n'y est pas, et lui affecte par
        défaut la valeur 0"""
        pres = False
        for i in self.noeuds:
            if i[0] == nom :
                pres = True
        if not pres :
            self.noeuds.append((nom, 0))
        else :
            print("Le noeud ", nom, " existe deja !")
    
    def ajouter_liste_noeuds(self,liste):
        """Fait appel à la fonction précédente pour ajouter tous les noeuds
        dont les noms sont présents dans liste au graphe"""
        
        for nom in liste:
            self.ajouter_noeud(nom)

    def ajouter_arc(self, noeud1, noeud2):
        """Ajoute un arc entre les deux noeuds si il n'en existe pas déjà et
           si les deux noeuds concernés sont déjà dans le graphe"""
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
            
    def ajouter_liste_arcs(self,liste):
        """Ajoute au graphe les arcs entre les couples de sommets présents dans
        liste en faisant appel à la fonction précédente"""
        
        for couple in liste:
            n1,n2 = couple
            self.ajouter_arc(n1,n2)
            
            
    def generer_graphe(self, nb_noeuds, p):
        """Génère un graphe de nb_noeuds sommets et où l'arc entre deux sommets
        a une probabilité p d'exister"""
           
        for i in range(nb_noeuds):
           self.ajouter_noeud((chr(ord("A")+i)))
        
        for n1 in self.noeuds:
           for n2 in self.noeuds:
               r = random.random()
               if r<p:
                   noeud1,_ = n1
                   noeud2,_ = n2
                   self.ajouter_arc(noeud1,noeud2)
                   
    def modifier_gain(self,noeud,valeur):
        
        for n in self.noeuds:
            nom,v = n
            
            if nom==noeud:
                if v!=valeur:
                    self.noeuds.append((nom,valeur))
                    self.noeuds.remove(n)
                
    def partage_aleatoire(self):
        """Propose un partage aléatoire, on suppose ici que les ressources à 
        partager sur chaque arc sont égales à 1"""
        
        noeuds_partages = []
        
        random.shuffle(self.arcs)
        #print("arcs melange:",arcs)
        for arc in self.arcs:
            n1,n2 = arc
            if (n1 not in noeuds_partages) and (n2 not in noeuds_partages):
                r = random.random()
                self.modifier_gain(n1,r)
                self.modifier_gain(n2,1-r)
                noeuds_partages.append(n1)
                noeuds_partages.append(n2)
                
                       
    def affiche(self):
        """Dessine le graphe"""
        G = nx.Graph()
        
        for n in self.noeuds:
            nom,_ = n
            G.add_node(nom,label=nom)
        for a in self.arcs:
            n1,n2 = a
            G.add_edge(n1,n2)
        
        nx.draw(G, with_labels=True, font_weight='bold')
        
        
        
