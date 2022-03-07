#graph
import networkx as nx
import random

class Graphe :

    def __init__(self) :
        self.noeuds = []
        self.arcs = []
        self.partage = []
        
    def get_valeur(self,noeud):
        
        for n in self.noeuds:
            nom,val = n
            if nom==noeud:
                return val
        print("Le noeud n'existe pas")
        
    def get_voisin(self,noeud):
        voisins = []
        
        for arc in self.arcs:
            n1,n2 = arc
            if n1==noeud:
                voisins.append(n2)
            if n2==noeud:
                voisins.append(n1)
        
        return voisins
    
    def offre_ext(self,n1):
        n2 = None
        offre = 0
        v1 = self.get_valeur(n1)
        
        voisins = self.get_voisin(n1)
        for v in voisins:
            v2 = self.get_valeur(v)
            valeur = (1-v1-v2)*0.5
            if valeur>offre:
                offre = valeur
                n2 = v
        
        return n2,offre
                

    def afficher_graphe(self):
        """Affiche les listes correspondant aux noeuds et aux arcs du graphe"""
        print("AFFICHAGE")
        print("Liste des noeuds : ", self.noeuds)
        print("Liste des arcs : ", self.arcs)
        print("Partage : ",self.partage)
        print()

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
        
        #si un noeud n'est relié à aucun autre, on le relie au premier de la liste
        #s'il il s'agit du premier noeud dans la liste on le relie au dernier
        for n in self.noeuds:
            seul = True
            nom,_ = n
            for a in self.arcs:
                n1,n2 = a
                if n1==nom or n2==nom:
                    seul = False
            if seul:
                print(nom,"seul")
                if n!=self.noeuds[0]:
                    n0,_ = self.noeuds[0]
                    self.ajouter_arc(nom,n0)
                else:
                    n1, _ = self.noeuds[1]
                    self.ajouter_arc(nom,n1)
        
                
                   
    def modifier_gain(self,noeud,valeur):
        
        for n in self.noeuds:
            nom,v = n
            
            if nom==noeud:
                if v!=valeur:
                    self.noeuds.append((nom,valeur))
                    self.noeuds.remove(n)
    
    def get_val_noeud(self, noeud):
        for i in self.noeuds:
            if i[0] == noeud :
                return i[1]
        return -1
                
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
                self.modifier_gain(n1,round(r,2))
                self.modifier_gain(n2,round(1-r,2))
                noeuds_partages.append(n1)
                noeuds_partages.append(n2)
                self.partage.append((n1,n2))
        print("noeuds partages=",noeuds_partages)
        #print("noeuds apres partage: ",self.noeuds)
        
    def est_stable(self):
        
        stable = True
        pas_stable = []
        #pour tout arc (n1,n2) qui n'est pas dans le partage, on verifie qu'un
        #partage entre n1 et n2 n'augmenterait pas la valeur des deux noeuds
        #si ce n'est pas le cas, partage n'est pas stable
        #print("noeuds test stabilite",self.noeuds)
        for arc in self.arcs:
            n1,n2 = arc
            if (n1,n2) not in self.partage and (n2,n1) not in self.partage:
                print("n1=",n1)
                print("n2=",n2)
                v1 = self.get_valeur(n1)
                v2 = self.get_valeur(n2)
                print("v1=",v1)
                print("v2=",v2)
                if (1-v2)>v1 and (1-v1)>v2:
                    stable = False
                    print(n1+" et "+n2+" pas stables")
                    pas_stable.append(n1)
                    pas_stable.append(n2)
                    #pas_stable.append((n1,n2))
        return stable, list(set(pas_stable))
    
    def devenir_stable(self,pas_stable):
        stable = False
        i = 0
        while not stable and i<20:
            self.afficher_graphe()
            for ps in pas_stable:
                
                n1,n2 = ps
                v1 = self.get_valeur(n1)
                v2 = self.get_valeur(n2)
                print("noeuds pas stables: "+n1+n2)
                for p in self.partage:
                    p1,p2 = p
                    if n1==p1 or n2==p1:
                        print("suppression ",p)
                        self.partage.remove(p)
                        self.modifier_gain(p2,0)
                        break
                    if n1==p2  or n2==p2:
                        print("suppression ",p)
                        self.partage.remove(p)
                        self.modifier_gain(p1,0)
                        break
                    
                if v1+((1-v1-v2)*0.5)>0.99:
                    self.modifier_gain(v1,1)
                    self.modifier_gain(v2,0)
                elif v2+((1-v1-v2)*0.5)>0.99:
                    self.modifier_gain(v1,0)
                    self.modifier_gain(v2,1)
                else:
                    self.modifier_gain(n1,v1+((1-v1-v2)*0.5))
                    self.modifier_gain(n2,v2+((1-v1-v2)*0.5))
                self.partage.append((n1,n2))
                print("noeuds apres modif:",self.noeuds)
                break
                
            stable,pas_stable = self.est_stable()
            i += 1
        if i<20:
            print("Le graphe est stable")
        else:
            print("Le graphe n'est toujours pas stable")
        self.afficher_graphe()
        
                       
    def affiche(self):
        """Dessine le graphe"""
        G = nx.Graph()
        
        for n in self.noeuds:
            nom,v = n
            G.add_node(nom,label=nom)
        for a in self.arcs:
            n1,n2 = a
            G.add_edge(n1,n2,weight=1)

        nx.draw(G, with_labels=True, font_weight='bold')
        
