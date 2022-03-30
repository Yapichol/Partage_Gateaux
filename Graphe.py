#graph
import networkx as nx
import random

class Graphe :

    def __init__(self) :
        self.noeuds = []
        self.arcs = []
        self.partage = []
        
    def get_valeur(self,noeud):
        """Retourne la valeur du noeud passe en parametres"""
        for n in self.noeuds:
            nom,val = n
            if nom==noeud:
                return val
        #print("Le noeud n'existe pas")
        
    def get_voisin(self,noeud):
        """Retourne la liste des voisins du noeud"""
        voisins = []
        
        for arc in self.arcs:
            n1,n2 = arc
            if n1==noeud:
                voisins.append(n2)
            if n2==noeud:
                voisins.append(n1)
        
        return voisins
    
    def offre_ext(self,n1,liste_noeuds):
        """Retourne le noeud de la liste qui offrira la meilleure offre au
        noeud ainsi que la valeur de l'offre"""
        n2 = None
        offre = 0
        
        voisins = self.get_voisin(n1)
        for n in liste_noeuds:
            if n in voisins:
                valeur = 1-self.get_valeur(n)
                if valeur>offre:
                    offre = valeur
                    n2 = n
        
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

	
	
    def changer_nom_noeud(self, nom, nouv_nom) :
        presNouv = False
        presAnci = False
        for i in self.noeuds:
            if i[0] == nouv_nom :
                presNouv = True
            if i[0] == nom :
                presAnci = True
        if (not presNouv) and (presAnci) :
            for i in range(len(self.noeuds)) :
                n, val =  self.noeuds[i]
                if nom == n :
                    self.noeuds[i] = (nouv_nom, val)
                    break
            for i in range(len(self.arcs)) :
                n1, n2 = self.arcs[i]
                if n1 == nom :
                    self.arcs[i] = (nouv_nom, n2)
                elif n2 == nom :
                    self.arcs[i] = (n1, nouv_nom)
            for i in range(len(self.partage)) :
                n1, n2 = self.partage[i]
                if n1 == nom :
                    self.partage[i] = (nouv_nom, n2)
                elif n2 == nom :
                    self.partage[i] = (n1, nouv_nom)
    
    
    
    def supprimer_noeud(self, nom) :
        pres = False
        for i in self.noeuds:
            if i[0] == nom :
                pres = True
        if pres :
            pos = -1
            for i in range(len(self.noeuds)) :
                n, val =  self.noeuds[i]
                if nom == n :
                    pos = i
            if pos != -1 :
                self.noeuds.pop(pos)
            listSuppr = []
            for i in range(len(self.arcs)) :
                n1, n2 = self.arcs[i]
                if (n1 == nom) or (n2 == nom):
                    listSuppr.append(i)
            diff = 0
            for i in listSuppr :
                self.arcs.pop(i - diff)
                diff += 1
            listSuppr = []
            for i in range(len(self.partage)) :
                n1, n2 = self.partage[i]
                if (n1 == nom):
                    listSuppr.append(i)
                    self.modifier_gain(n2, 0)
                elif (n2 == nom):
                    listSuppr.append(i)
                    self.modifier_gain(n1, 0)
            diff = 0
            for i in listSuppr :
                self.partage.pop(i - diff)
                diff += 1
    
    
    
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
    
    
    
    def supprimer_arc(self, arc) :
        pos = -1
        for i in range(len(self.arcs)) :
            n1, n2 = self.arcs[i]
            if ((n1, n2) == arc) or ((n2, n1) == arc):
                pos = i
        if pos != -1 :
            self.arcs.pop(pos)
            pos = -1
        for i in range(len(self.partage)) :
            n1, n2 = self.partage[i]
            if ((n1, n2) == arc) or ((n2, n1) == arc):
                pos = i
                self.modifier_gain(n1, 0)
                self.modifier_gain(n2, 0)
        if pos != -1 :
            self.partage.pop(pos)
    
    
    
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
                #print(nom,"seul")
                if n!=self.noeuds[0]:
                    n0,_ = self.noeuds[0]
                    self.ajouter_arc(nom,n0)
                else:
                    n1, _ = self.noeuds[1]
                    self.ajouter_arc(nom,n1)
        
                
                   
    def modifier_gain(self,noeud,valeur):
        """Modifie la valeur du noeud dans le graphe"""
        for n in self.noeuds:
            nom,v = n
            
            if nom==noeud:
                if v!=valeur:
                    self.noeuds.append((nom,valeur))
                    self.noeuds.remove(n)
	
    
    
    def modifier_partage(self, arc, val_noeud1, val_noeud2):
        """Cree un partage entre les noeuds concernes par l'arc passe en parametre,
        val_noeud1 est attribue au premier noeud du de l'arc et val_noeud2 au second,
        le partage est mis a niveau par rapport au poids de l'arc"""
        if (arc not in self.arcs) and ((arc[1], arc[0]) not in self.arcs) :
            print("Arc inexistant")
            return -1
        poidarc = 1
        val_n1 = 0
        val_n2 = 0
        if val_noeud1 + val_noeud2 > 0 :
            val_n1 = (val_noeud1 / (val_noeud1 + val_noeud2)) * poidarc
            val_n2 = (val_noeud2 / (val_noeud1 + val_noeud2)) * poidarc
        change = (-1, -1)
        for i in range(len(self.partage)) :
            n1, n2 = self.partage[i]
            if (arc[0] == n1 and arc[1] != n2) or (arc[1] == n1 and arc[0] != n2) or (arc[0] != n1 and arc[1] == n2) or (arc[1] != n1 and arc[0] == n2):
                if change[0] == -1 :
                    change = (i, -1)
                else :
                    ch0 = change[0]
                    change = (ch0, i)
        #print(self.partage)
        #print(change)
        if change[0] > -1 :
            self.modifier_gain(self.partage[change[0]][0], 0)
            self.modifier_gain(self.partage[change[0]][1], 0)
            #self.dicLigne[self.graphe.partage[change[0]]] = 0
            self.partage[change[0]] = arc
            if change[1] > -1 :
                self.modifier_gain(self.partage[change[1]][0], 0)
                self.modifier_gain(self.partage[change[1]][1], 0)
                #self.dicLigne[self.partage[change[1]]] = 0
                self.partage.pop(change[1])
        elif (arc not in self.partage) and ((arc[1], arc[0]) not in self.partage) :
            self.partage.append(arc)
        #self.dicLigne[arc] = 1
        self.modifier_gain(arc[0], val_n1)
        self.modifier_gain(arc[1], val_n2)
    
	
	
    def supprimer_partage(self, arc):
        if (arc in self.partage) :
            self.modifier_gain(arc[0], 0)
            self.modifier_gain(arc[1], 0)
            self.partage.remove(arc)
        if(arc[1], arc[0]) in self.partage :
            self.modifier_gain(arc[0], 0)
            self.modifier_gain(arc[1], 0)
            self.partage.remove((arc[1], arc[0]))
	
	
	
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
        #print("noeuds partages=",noeuds_partages)
        #print("noeuds apres partage: ",self.noeuds)
        
    def est_stable(self):
        """Retourn True et une liste vide si le partage est stable, False et la 
        liste des noeuds non stables sinon"""
        
        stable = True
        pas_stable = []
        paires = []
        #pour tout arc (n1,n2) qui n'est pas dans le partage, on verifie qu'un
        #partage entre n1 et n2 n'augmenterait pas la valeur des deux noeuds
        #si ce n'est pas le cas, partage n'est pas stable
        #print("noeuds test stabilite",self.noeuds)
        for arc in self.arcs:
            n1,n2 = arc
            if (n1,n2) not in self.partage and (n2,n1) not in self.partage:

                v1 = self.get_valeur(n1)
                v2 = self.get_valeur(n2)

                if (1-v2)>v1 and (1-v1)>v2:
                    stable = False
                    pas_stable.append(n1)
                    pas_stable.append(n2)
                    paires.append((n1,n2))
        return stable, list(set(pas_stable)),paires
    
    def devenir_stable(self,pas_stable,paires):
        
        while pas_stable:
            n1 = pas_stable.pop(0)
            n2 = None
            options = []
            for o in paires:
                x1,x2 = o
                if x1==n1 and (x2 in pas_stable):
                    options.append(x2)
                    paires.remove(o)
                if x2==n1 and (x1 in pas_stable):
                    options.append(x1)
                    paires.remove(o)
            n2,offre = self.offre_ext(n1,options)
            v1 = self.get_valeur(n1)
            
            
            if n2!=None and ((n1,n2) not in self.partage) and ((n2,n1) not in self.partage):
                v2 = self.get_valeur(n2)
                pas_stable.remove(n2)
                #on supprime les partages qui existaient entre n1 et 
                #les autres noeuds du graphe
                for p in self.partage:
                    p1,p2 = p
                    if n1==p1:
                        self.partage.remove(p)
                        self.modifier_gain(p2,0)
                        break
                    if n1==p2:
                        self.partage.remove(p)
                        self.modifier_gain(p1,0)
                        break
                #on supprime les partages qui existaient entre n2 et 
                #les autres noeuds du graphe
                for p in self.partage:
                    p1,p2 = p
                    if n2==p1:
                        self.partage.remove(p)
                        self.modifier_gain(p2,0)
                        break
                    if n2==p2:
                        self.partage.remove(p)
                        self.modifier_gain(p1,0)
                        break
                
                #on considère que si un noeud arrive a obtenir plus que
                #0.99 il arrivera à obtenir 1
                v1 = v1+((1-v1-v2)*0.5)
                v2 = 1-v1
                if v1<=0.01:
                    self.modifier_gain(n1,0)
                    self.modifier_gain(n2,1)
                elif v2<=0.01:
                    self.modifier_gain(n1,1)
                    self.modifier_gain(n2,0)
                else:
                    self.modifier_gain(n1,v1)
                    self.modifier_gain(n2,v2)
                self.partage.append((n1,n2))
                       
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
        
