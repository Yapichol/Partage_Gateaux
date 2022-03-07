import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Canvas import *
import resources
import time



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

        close = fileMenu.addAction(QIcon(":/icons/quit.png"), "&Quit", self.quit, QKeySequence("Ctrl+Q"))
        fileBar.addAction(close)



        modeToolBar = QToolBar("Navigation")

        self.addToolBar( modeToolBar )
        actMove = modeToolBar.addAction( QIcon(":/icons/move.png"), "&Move", self.move )
        actZoomin = modeToolBar.addAction( QIcon(":/icons/zoom-in.png"), "&Move", self.zoomin )
        actZoomout = modeToolBar.addAction( QIcon(":/icons/zoom-out.png"), "&Move", self.zoomout )

        self.canvas = Canvas()
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.canvas)
        container = QWidget()
        container.setLayout(v_layout)
        self.setCentralWidget(container)


    ##############
    def imp(self):
        print("Import...")
        filename = QFileDialog.getOpenFileName(self,"Open File")
	    #print(filename)
        fi,a = filename

    def import_graph(self, graphe):
        self.canvas.imp_g(graphe)
        
    def exp(self):
        print("Export...")
        pass

    def move(self):
        print("Move...")
        self.canvas.set_mode("Move")

    def stab(self):
        print("Stable...")
        pass

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

    def quit(self):
        print("Quit")
        self.close()

    def closeEvent(self, event):
        reponse = QMessageBox.question(self, "Quitter", "Voulez-vous quitter ?" )
        if reponse == QMessageBox.Yes:
            event.accept()
        else :
            event.ignore()
    ##############
