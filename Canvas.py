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
		self.pointer = None
        
		self.setMinimumSize(800, 500)
		self.posCanvas = (0,0)
		self.cursorPosPress = None
		self.cursorPosRelease = None
		self.mode = "Move"              # mode 
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
		for n1,n2 in self.graphe.arcs :
			if ((n1,n2) in self.graphe.partage) or ((n2,n1) in self.graphe.partage):
				self.dicLigne[(n1,n2)] = 1
			else :
				self.dicLigne[(n1,n2)] = 0
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
	
	def maj_graph(self, graph):
		self.graphe = graph
		for i in self.graphe.noeuds :
			nom, val = i
			if nom not in self.dicNoeuds :
				self.dicNoeuds[nom] = QPoint(0, 0)
		for i in self.graphe.arcs :
			n1, n2 = i
			if ((n1, n2) in self.graphe.partage) or ((n2, n1) in self.graphe.partage) :
				self.dicLigne[i] = 1
			else :
				self.dicLigne[i] = 0
				
		self.update()
		
	def modif_partage(self, arc) :
		val_noeud1 = 0
		val_noeud2 = 0
		if (val_noeud1 + val_noeud2 > 0) :
			self.graphe.modifier_partage(arc, val_noeud1, val_noeud2)
		else :
			self.graphe.supprimer_partage(arc)
		self.maj_graph(self.graphe)
		"""
		if (arc not in self.graphe.arcs) and ((arc[1], arc[0]) not in self.graph.arcs):
			print("Arc inexistant")
			return -1
		poidarc = 1                  # A MODIFIER LORSQUE LES ARCS AURONT DES POIDS DIFFERENTS
		#                BOITE DE DIALOGUE POUR OBTENIR LA VALEUR
		val_noeud1 = self.graphe.get_valeur(arc[1])
		val_noeud2 = self.graphe.get_valeur(arc[0])
		if val_noeud1 + val_noeud2 == 0 :
			val_n1 = 0
			val_n2 = 0
			if arc in self.graphe.partage :
				self.graphe.partage.remove(arc)
			elif (arc[1], arc[0]) in self.graphe.partage :
				self.graphe.partage.remove((arc[1], arc[0]))
			self.dicLigne[arc] = 0

		else :
			val_n1 = (val_noeud1 / (val_noeud1 + val_noeud2)) * poidarc
			val_n2 = (val_noeud2 / (val_noeud1 + val_noeud2)) * poidarc
			change = (-1, -1)
			for i in range(len(self.graphe.partage)):
				n1, n2 = self.graphe.partage[i]
				if (arc[0] == n1 and arc[1] != n2) or (arc[1] == n1 and arc[0] != n2) or (arc[0] != n1 and arc[1] == n2) or (arc[1] != n1 and arc[0] == n2):
					if change[0] == -1 :
						change = (i, -1)
					else :
						ch0 = change[0]
						change = (ch0, i)
			print(self.graphe.partage)
			print(change)
			if change[0] > -1 :
				self.graphe.modifier_gain(self.graphe.partage[change[0]][0], 0)
				self.graphe.modifier_gain(self.graphe.partage[change[0]][1], 0)
				self.dicLigne[self.graphe.partage[change[0]]] = 0
				self.graphe.partage[change[0]] = arc
				if change[1] > -1 :
					self.graphe.modifier_gain(self.graphe.partage[change[1]][0], 0)
					self.graphe.modifier_gain(self.graphe.partage[change[1]][1], 0)
					self.dicLigne[self.graphe.partage[change[1]]] = 0
					self.graphe.partage.pop(change[1])
			elif (arc not in self.graphe.partage) and ((arc[1], arc[0]) not in self.graphe.partage) :
				self.graphe.partage.append(arc)
			self.dicLigne[arc] = 1
			self.graphe.modifier_gain(arc[0], val_n1)
			self.graphe.modifier_gain(arc[1], val_n2)"""


	def set_mode(self, mode):
		self.mode = mode
	
	def mousePressEvent(self, event):
		pointpress = event.pos()
		if self.mode == "Draw" :
			self.cursorPosPress = QPoint(pointpress.x() - self.posCanvas[0], pointpress.y() - self.posCanvas[1])
			self.pointer = (QLineF(self.cursorPosPress.x() - 4, self.cursorPosPress.y(), self.cursorPosPress.x() + 4, self.cursorPosPress.y()), QLineF(self.cursorPosPress.x(), self.cursorPosPress.y() - 4, self.cursorPosPress.x(), self.cursorPosPress.y() + 4))
		#elif self.mode == "Move" :
		#	self.cursorPosPress = QPoint(pointpress.x() - self.posCanvas[0], pointpress.y() - self.posCanvas[1])
		#	self.cursorPosRelease = self.cursorPosPress
		elif self.mode == "Move" :
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
			self.pointer = (QLineF(self.cursorPosRelease.x() - 4, self.cursorPosRelease.y(), self.cursorPosRelease.x() + 4, self.cursorPosRelease.y()), QLineF(self.cursorPosRelease.x(), self.cursorPosRelease.y() - 4, self.cursorPosRelease.x(), self.cursorPosRelease.y() + 4))
			intersection = QPointF(0, 0)
			arc = (".", ".")
			for cle, valeur in self.dicLigne.items():
				n1, n2 = cle
				ligne = QLineF(QPoint(self.dicNoeuds[n1].x() + int(self.tailleNoeud / 2), self.dicNoeuds[n1].y() + int(self.tailleNoeud / 2)), QPoint(self.dicNoeuds[n2].x() + int(self.tailleNoeud / 2), self.dicNoeuds[n2].y() + int(self.tailleNoeud / 2)))
				if (ligne.intersect(self.pointer[0], intersection) == 1) or (ligne.intersect(self.pointer[1], intersection) == 1) :
					print(cle)
					arc = cle
					break
					#print("INTERSECTION :(", intersection.x()," , ", intersection.y(), ")")
					#print("POINTEUR :(", self.cursorPosRelease.x()," , ", self.cursorPosRelease.y(), ")")
			if arc != (".", ".") :
				self.modif_partage(arc)
				print("Fin 2")
			#self.pointer = None
		#elif self.mode == "Move" :
		#	self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
		#	self.posCanvas = (self.posCanvas[0] + self.cursorPosRelease.x() - self.cursorPosPress.x(), self.posCanvas[1] + self.cursorPosRelease.y() - self.cursorPosPress.y())
		elif self.mode == "Move" :
			self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
			self.listSelected = []
		self.update()
	
	def mouseMoveEvent(self, event):
		pointrelease = event.pos()
		if self.mode == "Draw" :
			self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
			self.pointer = (QLineF(self.cursorPosRelease.x() - 4, self.cursorPosRelease.y(), self.cursorPosRelease.x() + 4, self.cursorPosRelease.y()), QLineF(self.cursorPosRelease.x(), self.cursorPosRelease.y() - 4, self.cursorPosRelease.x(), self.cursorPosRelease.y() + 4))

		#elif self.mode == "Move" :
		#	self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
		#	self.posCanvas = (self.posCanvas[0] + self.cursorPosRelease.x() - self.cursorPosPress.x(), self.posCanvas[1] + self.cursorPosRelease.y() - self.cursorPosPress.y())
		elif self.mode == "Move" :
			ancienPos = self.cursorPosRelease
			self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
			if self.listSelected != []:
				for i in self.listSelected :
					pos = self.dicNoeuds[i]
					self.dicNoeuds[i] = QPoint(pos.x() + self.cursorPosRelease.x() - ancienPos.x(), pos.y() + self.cursorPosRelease.y() - ancienPos.y())
			else :
				self.posCanvas = (self.posCanvas[0] + self.cursorPosRelease.x() - self.cursorPosPress.x(), self.posCanvas[1] + self.cursorPosRelease.y() - self.cursorPosPress.y())
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
		"""if self.mode == "Draw" :
			painter.drawLine(self.pointer[0])
			painter.drawLine(self.pointer[1])"""
					




