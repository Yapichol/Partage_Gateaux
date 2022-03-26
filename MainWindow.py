import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
from Canvas import *
from Graphe import *
import resources
import time
import os


class MainWindow(QMainWindow):

    def __init__(self, parent = None ):
        QMainWindow.__init__(self, parent )
        print( "init mainwindow")
        self.resize(600, 500)

        bar = self.menuBar()
        fileMenu = bar.addMenu("File")
        toolsMenu = bar.addMenu("Tools")

        fileBar = QToolBar("File")
        self.addToolBar(fileBar)


        cr = QAction(QIcon(),"Create...",self)
        cr.setShortcut(QKeySequence("Ctrl+C"))
        cr.setToolTip("Create")
        cr.setStatusTip("Create")
        fileMenu.addAction(cr)
        cr.triggered.connect(self.create)

        im = QAction(QIcon(),"Import...",self)
        im.setShortcut(QKeySequence("Ctrl+O"))
        im.setToolTip("Import")
        im.setStatusTip("Import")
        fileMenu.addAction(im)
        im.triggered.connect(self.imp)

        ex = QAction(QIcon(),"Export...",self)
        ex.setShortcut(QKeySequence("Ctrl+E"))
        ex.setToolTip("Export")
        ex.setStatusTip("Export")
        fileMenu.addAction(ex)
        ex.triggered.connect(self.exp)

        exas = QAction(QIcon(),"Export as...",self)
        exas.setShortcut(QKeySequence("Ctrl+R"))
        exas.setToolTip("Export as")
        exas.setStatusTip("Export as")
        fileMenu.addAction(exas)
        exas.triggered.connect(self.expas)

        alea = QAction(QIcon(),"Graphe Aléatoire...",self)
        alea.setShortcut(QKeySequence("Ctrl+A"))
        alea.setToolTip("Graphe Aléatoire")
        alea.setStatusTip("Graphe Aléatoire")
        fileMenu.addAction(alea)
        alea.triggered.connect(self.alea)

        stable = QAction(QIcon(),"Verif stable...",self)
        stable.setShortcut(QKeySequence("Ctrl+S"))
        stable.setToolTip("Stable")
        stable.setStatusTip("Stable")
        toolsMenu.addAction(stable)
        stable.triggered.connect(self.stab)

        balanced = QAction(QIcon(),"Verif balanced...",self)
        balanced.setShortcut(QKeySequence("Ctrl+B"))
        balanced.setToolTip("Balanced")
        balanced.setStatusTip("Balanced")
        toolsMenu.addAction(balanced)
        balanced.triggered.connect(self.bal)

        rend_stable = QAction(QIcon(),"Rend stable...",self)
        rend_stable.setShortcut(QKeySequence("Ctrl+R"))
        rend_stable.setToolTip("Rend Stable")
        rend_stable.setStatusTip("Rend stable")
        toolsMenu.addAction(rend_stable)
        rend_stable.triggered.connect(self.rend_stable)

        close = fileMenu.addAction(QIcon(":/icons/quit.png"), "&Quit", self.quit, QKeySequence("Ctrl+Q"))
        fileBar.addAction(close)



        modeToolBar = QToolBar("Navigation")


        self.addToolBar( modeToolBar )
        actMove = modeToolBar.addAction( QIcon(":/icons/move.png"), "&Move", self.move)
        actDraw = modeToolBar.addAction( QIcon(":/icons/draw.png"), "&Draw", self.draw)
        actSelect = modeToolBar.addAction( QIcon(":/icons/select.png"), "&Select", self.select)
        actZoomin = modeToolBar.addAction( QIcon(":/icons/zoom-in.png"), "&Zoomin", self.zoomin)
        actZoomout = modeToolBar.addAction( QIcon(":/icons/zoom-out.png"), "&Zoomout", self.zoomout)
        actPause = modeToolBar.addAction(QtGui.QIcon("./icons/pause.png"),"&Pause", self.pause)
        actResume = modeToolBar.addAction(QtGui.QIcon("./icons/resume.png"),"&Resume", self.resume)
        actStop = modeToolBar.addAction(QtGui.QIcon("./icons/stop.png"),"&Stop", self.stop)
        
        self.canvas = Canvas()
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.canvas)
        container = QWidget()
        container.setLayout(v_layout)
        self.setCentralWidget(container)
        


    ##############
    def imp(self):
        self.s = True
        print("Import...")
        g = Graphe()
        filename = QFileDialog.getOpenFileName(self,"Open File")
	    #print(filename)
        fi,a = filename

        data = open(fi, "r")

        nbsommets = int(data.readline())
        nbarcs = int(data.readline())

        doc = data.readlines()

        for i in range(0,nbsommets):
            tmp = doc[i]
            tmp = tmp.replace(',','')
            tmp = tmp.replace(' ','')
            tmp = tmp.replace('\n','')
            lettre = tmp[0]
            valeur = float(tmp[1:])
            g.ajouter_noeud(lettre)
            g.modifier_gain(lettre,valeur)

        for i in range(nbsommets,nbsommets+nbarcs):
            arc = str(doc[i])
            arc=arc.replace(' ','')
            arc=arc.replace(',','')
            g.ajouter_arc(arc[0],arc[1])
        
        for i in range(nbsommets+nbarcs,len(doc)):
            partage = str(doc[i])
            partage=partage.replace(' ','')
            partage=partage.replace(',','')
            g.partage.append((partage[0],partage[1]))
		
        self.import_graph(g)

    def import_graph(self, graphe):
        
        self.canvas.imp_g(graphe)
        
    def exp(self):
        print("Export...")

        
        path, dirs, files = next(os.walk("./graphes"))
        file_count = len(files)
            
        name = "graphe"+str(file_count)+".txt"
        
        with open('graphes/'+name,'w') as f:
            f.write(str(len(self.canvas.graphe.noeuds))+'\n')
            f.write(str(len(self.canvas.graphe.arcs))+'\n')

            for i in self.canvas.graphe.noeuds :
                lettre,valeur = i
                f.write(lettre+','+str(valeur)+'\n')

            for i in self.canvas.graphe.arcs:
                lettre1,lettre2 = i
                f.write(lettre1+','+lettre2+'\n')

            for i in self.canvas.graphe.partage:
                lettre1,lettre2 = i
                f.write(lettre1+','+lettre2+'\n')

            msg = QMessageBox()
            msg.setText("Le graphe a bien été exporté")
            msg.exec()  

    def expas(self):
        filename = QFileDialog.getSaveFileName(self,"Save File")	
        fi,a = filename
        print(filename)
        if len(fi) >2 :
			
            with open(str(fi)+".txt","w") as f:
                f.write(str(len(self.canvas.graphe.noeuds))+'\n')
                f.write(str(len(self.canvas.graphe.arcs))+'\n')

                for i in self.canvas.graphe.noeuds :
                    lettre,valeur = i
                    f.write(lettre+','+str(valeur)+'\n')

                for i in self.canvas.graphe.arcs:
                    lettre1,lettre2 = i
                    f.write(lettre1+','+lettre2+'\n')

                for i in self.canvas.graphe.partage:
                    lettre1,lettre2 = i
                    f.write(lettre1+','+lettre2+'\n')
            
        
    def alea(self):
        self.s = True
        g = Graphe()
        #nbsommets = random.randint(2,10)
        #arcs=random.uniform(0,0.5)
        #g.generer_graphe(nbsommets,arcs)
        g.generer_graphe(5,0.2)
        g.partage_aleatoire()
        self.import_graph(g)

    def move(self):
        if self.canvas.mode != "Calcul" :
            print("Move...")
            self.canvas.set_mode("Move")

    def stab(self):
        print("Stable...")
        boole,liste = self.canvas.graphe.est_stable()
        if boole :
            good = QMessageBox()
            good.setText("Ce graphe est stable")
            good.exec()
        else :
            bad = QMessageBox()
            bad.setText("Ce graphe n'est pas stable")
            bad.exec()  
            self.rend_stable()           
        #print(self.canvas.graphe.est_stable())

    def bal(self):
        print("Balanced...")
        pass

    def create(self):
        print("Create...")
        pass

    def zoomin(self):
        print("Zoom in...")
        pass

    def zoomout(self):
        print("Zoom out...")
        pass

    def pause(self):
        self.p = True

    def stop(self):
        self.s = True

    def resume(self):
        self.r = True

    def quit(self):
        print("Quit")
        self.close()

    def closeEvent(self, event):
        reponse = QMessageBox.question(self, "Quitter", "Voulez-vous quitter ?" )
        if reponse == QMessageBox.Yes:
            event.accept()
        else :
            event.ignore()


    def draw(self):
        if self.canvas.mode != "Calcul" :
            print("Draw...")
            self.canvas.set_mode("Draw")

    def select(self):
        if self.canvas.mode != "Calcul" :
            print("Select...")
            self.canvas.set_mode("Select")


    def rend_stable(self):
        self.canvas.set_mode("Calcul")
        affiche = False
        self.p = False
        self.r = False
        self.s = False
        boole, liste = self.canvas.graphe.est_stable()
        iter_max = 100
        n = 0
        if boole :
            good = QMessageBox()
            good.setText("Ce graphe est stable")
            good.exec()
            #print("Ce graphe est stable")
        else :

            reponse = QMessageBox.question(self, "Stabilité", "Voulez-vous rendre ce graphe stable ?" )
            if reponse == QMessageBox.Yes:
                affichage = QMessageBox.question(self, "Stabilité", "Voulez-vous afficher chaque itération?" )
                if affichage == QMessageBox.Yes:
                    affiche = True
                    
                while not boole :
                    n+=1
                    g=self.canvas.graphe
                    #print("partage: ",g.partage)
                    g.devenir_stable(liste)
                    #self.import_graph(g)
                    self.canvas.maj_graph(g)
                    if affiche:
                        self.canvas.repaint()
                        loop = QEventLoop()
                        QTimer.singleShot(2000, loop.quit)
                        loop.exec_()
                    boole, liste = g.est_stable()

                    while self.p and not self.s:
                        loop = QEventLoop()
                        QTimer.singleShot(2000, loop.quit)
                        loop.exec_()
                        if self.r or self.s:
                            self.r = False
                            break
                    self.p = False

                    if n>iter_max or self.s:
                        
                        break
                        
                if boole :
                    good = QMessageBox()
                    good.setText("Ce graphe est stable en "+str(n)+" itérations.")
                    good.exec()
                    #print("Ce graphe est stable")
                elif not self.s:
                    bad = QMessageBox()
                    bad.setText("Impossible de rendre ce graphe stable")
                    bad.exec()
                    #print("Impossible de rendre ce graphe stable")
                else:
                    self.s = False
                    bad = QMessageBox()
                    bad.setText("Processus arrêté")
                    bad.exec()
        self.canvas.set_mode("Move")


    ##############



