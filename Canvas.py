from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Graphe import *
import math


class Canvas(QWidget):
	
	def __init__(self, parent = None):
		print("class Canvas")
		QWidget.__init__(self, parent)
		
		self.dicNoeuds = {}
		self.dicLigne = {}
		self.graphe = None
        
		self.setMinimumSize(800, 500)
		self.posCanvas = (0,0)
		self.cursorPosPress = None
		self.cursorPosRelease = None
		self.mode = "Select"              # mode 
		self.listSelected = []          # liste des elements selectionnes
		self.tailleNoeud = 35
	
	
	def get_listElem(self):
		return self.listElem
	
	def reset(self):
		print("reset")
	
	def imp_g(self, graphe):
		self.graphe = graphe
		self.dicNoeuds = {}
		self.dicLigne = {}
		for i in self.graphe.noeuds :
			self.dicNoeuds[i[0]] = QPoint(0, 0)
		for i in self.graphe.arcs :
			self.dicLigne[i] = 0
		repartieAuto = True
		if repartieAuto :
			roue = 0
			for cle, val in self.dicNoeuds.items() :
				if roue > 7 :
					roue = 0
				bouge = 1
				while bouge == 1 :
					bouge = 0
					for cle2, val2 in self.dicNoeuds.items() :
						if cle2 != cle and math.sqrt(((self.dicNoeuds[cle].x() - val2.x()) ** 2) + ((self.dicNoeuds[cle].y() - val2.y()) ** 2)) < 150:
							#print(math.sqrt(((val.x() - val2.x()) ** 2) + ((val.y() - val2.y()) ** 2)))
							bouge = 1
					if bouge == 1:
						if roue == 0:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x() + 10, pos.y())
						elif roue == 1:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x() + 10, pos.y() + 10)
						elif roue == 2:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x(), pos.y() + 10)
						elif roue == 3:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x() - 10, pos.y() + 10)
						elif roue == 4:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x() - 10, pos.y())
						elif roue == 5:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x() - 10, pos.y() - 10)
						elif roue == 6:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x(), pos.y() - 10)
						elif roue == 7:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x() + 10, pos.y() - 10)
				roue += 1
		self.update()
	
	
	def set_mode(self, mode):
		self.mode = mode
	
	def mousePressEvent(self, event):
		pointpress = event.pos()
		if self.mode == "Draw" :
			self.cursorPosPress = QPoint(pointpress.x() - self.posCanvas[0], pointpress.y() - self.posCanvas[1])
		elif self.mode == "Move" :
			self.cursorPosPress = QPoint(pointpress.x() - self.posCanvas[0], pointpress.y() - self.posCanvas[1])
			self.cursorPosRelease = self.cursorPosPress
		elif self.mode == "Select" :
			self.listSelected = []
			self.cursorPosPress = QPoint(pointpress.x() - self.posCanvas[0], pointpress.y() - self.posCanvas[1])
			self.cursorPosRelease = self.cursorPosPress
			if self.dicNoeuds != {} :
				for cle, valeur in self.dicNoeuds.items():
					rec = QRect(valeur.x(), valeur.y(), self.tailleNoeud, self.tailleNoeud)
					if rec.contains(self.cursorPosPress.x(), self.cursorPosPress.y()) :
						self.listSelected.append(cle)
						break
		self.update()
	
	def mouseReleaseEvent(self, event):
		pointrelease = event.pos()
		if self.mode == "Draw" :
			self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
		elif self.mode == "Move" :
			self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
			self.posCanvas = (self.posCanvas[0] + self.cursorPosRelease.x() - self.cursorPosPress.x(), self.posCanvas[1] + self.cursorPosRelease.y() - self.cursorPosPress.y())
		elif self.mode == "Select" :
			self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
			self.listSelected = []
		self.update()
	
	def mouseMoveEvent(self, event):
		pointrelease = event.pos()
		if self.mode == "Draw" :
			self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
		elif self.mode == "Move" :
			self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
			self.posCanvas = (self.posCanvas[0] + self.cursorPosRelease.x() - self.cursorPosPress.x(), self.posCanvas[1] + self.cursorPosRelease.y() - self.cursorPosPress.y())
		elif self.mode == "Select" :
			ancienPos = self.cursorPosRelease
			self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
			if self.listSelected != []:
				for i in self.listSelected :
					pos = self.dicNoeuds[i]
					self.dicNoeuds[i] = QPoint(pos.x() + self.cursorPosRelease.x() - ancienPos.x(), pos.y() + self.cursorPosRelease.y() - ancienPos.y())
			#else :
				#self.posCanvas = (self.posCanvas[0] + self.cursorPosRelease.x() - self.cursorPosPress.x(), self.posCanvas[1] + self.cursorPosRelease.y() - self.cursorPosPress.y())
		self.update()
	
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.translate(QPoint(self.posCanvas[0], self.posCanvas[1]))
		pen = QPen(Qt.black)
		pen.setWidth(3)
		painter.setPen(pen)
		for cle, valeur in self.dicLigne.items() :
			if cle != None or valeur != None :
				n1, n2 = cle 
				if valeur == 1 :
					pen2 = QPen(Qt.red)
					pen2.setWidth(3)
					painter.setPen(pen2)
				painter.drawLine(QPoint(self.dicNoeuds[n1].x() + int(self.tailleNoeud / 2), self.dicNoeuds[n1].y() + int(self.tailleNoeud / 2)), QPoint(self.dicNoeuds[n2].x() + int(self.tailleNoeud / 2), self.dicNoeuds[n2].y() + int(self.tailleNoeud / 2)))
				if valeur == 1 :
					pen = QPen(Qt.black)
					pen.setWidth(3)
					painter.setPen(pen)
		for cle, valeur in self.dicNoeuds.items() :
			painter.setBrush(Qt.white)
			if cle != None or valeur != None :
				painter.drawEllipse(valeur.x(), valeur.y(), self.tailleNoeud, self.tailleNoeud)
				painter.drawText(valeur.x(), valeur.y(), self.tailleNoeud, self.tailleNoeud, Qt.AlignCenter, cle)
				val = self.graphe.get_val_noeud(cle)
				if val != 0 :
					pen2 = QPen(Qt.red)
					pen2.setWidth(3)
					painter.setPen(pen2)
					if len(str(val)) > 10:
						painter.drawText(valeur.x() - self.tailleNoeud, valeur.y() - 15, 3 * self.tailleNoeud, 15, Qt.AlignLeft, str(val))
					else :
						painter.drawText(valeur.x() - self.tailleNoeud, valeur.y() - 15, 3 * self.tailleNoeud, 15, Qt.AlignCenter, str(val))
					pen = QPen(Qt.black)
					pen.setWidth(3)
					painter.setPen(pen)




