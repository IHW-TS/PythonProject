#!/usr/local/bin/python3
# -*-coding:utf-8 -*

from random import shuffle
from math import ceil,floor
from collections import OrderedDict
import time

class Taquin:
	def __init__(self, environment, previous=None, move=None):
		self.environment = environment
		self.environment.createdTaquins += 1
		self.previous = previous
		self.inv = None
		self.dis = None
		self.man = None
		self.h = None
		if previous == None:
			self.path = "_"
			self.g = 0
			self.sequence = self.magic(1)
		else:
			self.path = previous.path + move
			self.g = previous.g + 1
			self.sequence = previous.sequence.copy()
			self.moveTile(move)
			self.inv,self.dis,self.man,self.h = self.details()
		self.moves = self.findMoves()
		self.f = self.h + self.g
	def coordinates(self, content=0):
		width = self.environment.sizes[0]
		if isinstance(content, list):
			return (width * content[1]) + content[0]
		else:
			index = self.sequence.index(content)
			y = ceil((index + 1) / width) - 1
			x = index - (y * width)
			return [x, y]

	def details(self):
		width, length = self.environment.sizes
		weightings = self.environment.weightings
		seq = self.sequence
		inv = 0
		dis = 0
		man = 0
		h = 0
		for weighting in weightings:
			k = 0
			stepH = 0
			for i in range(0,length):
				stepMan = 0
				if weighting == weightings[0]:
					for j in range(i+1,length):
						if seq[i] != 0 and seq[j] != 0 and seq[i] > seq[j]:
							inv += 1
					if seq[i] != 0 and seq[i] != (i+1):
						dis += 1
				if i > 0:
					pos = self.coordinates(i)
					x = i % width
					coords = (((width - 1) if x == 0 else (x - 1)), ceil(i / width) - 1)
					stepMan += (abs(pos[0] - coords[0]) + abs(pos[1] - coords[1]))
					if weighting == weightings[0]:
						man += stepMan
					stepH += weighting[0][k] * stepMan
					k += 1
			if weighting[2] == 7:
				stepH += dis
			stepH = int(stepH / weighting[1])
			h += stepH
		h = int( h / len(weightings) )
		return [inv,dis,man,h]

	def findMoves(self,flex=False):
		limit = self.environment.sizes[0] - 1
		coords = self.coordinates()
		last = self.path[self.g]
		moves = []
		if coords[0] != 0 	  and (last != 'L' or flex): moves.append('R')
		if coords[0] != limit and (last != 'R' or flex): moves.append('L')
		if coords[1] != 0	  and (last != 'U' or flex): moves.append('D')
		if coords[1] != limit and (last != 'D' or flex): moves.append('U')
		return moves
	def moveTile(self, move):
		seq = self.sequence
		width = self.environment.sizes[0]
		x = self.coordinates(self.coordinates())
		if move == 'R': y = x - 1
		if move == 'L': y = x + 1
		if move == 'D': y = x - width
		if move == 'U': y = x + width
		seq[x] = seq[y]
		seq[y] = 0
	def valid(self):
		width = self.environment.sizes[0]
		self.inv,self.dis,self.man,self.h = self.details()
		row = abs(self.coordinates()[1] - width)
		return True if (((width % 2 == 1) and (self.inv % 2 == 0)) or ((width % 2 == 0) and ((row % 2 == 1) == (self.inv % 2 == 0)))) else False
	def children(self):
		childList = []
		for move in self.moves:
			child = Taquin(self.environment,self,move)
			if child.dis == 0:
				return child
			i = 0
			while (i < len(childList)):
				if (child.f < childList[i].f):
					break
				i += 1
			childList.insert(i,child)
		return childList
	def magic(self, rand=0):
		length = self.environment.sizes[1]
		seq = [0]*length
		for i in range(1, length):
			seq[i-1] = i
		if rand == 1:
			shuffle(seq)
			self.sequence = seq
			while not self.valid():
				shuffle(seq)
				self.sequence = seq
		return seq
	def traceroute(self):
		path = [self]
		while (isinstance(path[0].previous,Taquin)):
			path.insert(0,path[0].previous)
		return path
	def __repr__(self):
		printable = ""
		printable += "\n"
		printable += "Taquin :\n"
		printable += ("|  seq. .. : {}\n").format(self.sequence)
		printable += ("|  path .. : {}\n").format(self.path)
		printable += ("|  inv. .. : {}\n").format(self.inv)
		printable += ("|  man. .. : {}\n").format(self.man)
		printable += ("|  moves . : {}\n").format(self.moves)
		printable += ("|  g ..... : {}\n").format(self.g)
		printable += ("|  h ..... : {}\n").format(self.h)
		printable += ("|  f ..... : {}\n").format(self.f)
		printable += ("|  created : {}\n").format(self.environment.createdTaquins)
		return printable


class Environment:
	def __init__(self,width,choices=None):
		self.createdTaquins = 0
		self.sizes = (width,width*width)
		self.choices = choices
		self.weightings = self.getWeightings(choices)
		self.moves = [Taquin(self)]
		self.end = []
	def getWeightings(self,choices):
		width = self.sizes[0]
		length = self.sizes[1] - 1
		if (choices == None):
			choices = [5]
		weightings = []
		weight = length
		for index in choices:
			rho = (4 if index % 2 != 0 else 1)
			pi = [0] * length
			if index == 1:
				if width == 3:
					pi = [36, 12, 12, 4, 1, 1, 4, 1]
				else:
					for y in range(0,width):
						for x in range(0,width):
							if x == y == width-1:
								pass
							else:
								if x == y == 0:
									pi[0] = width * (width*3)
									x += 1
								if y == 0:
									while x < width:
										pi[x] = width * 3
										x += 1
								else:
									if (x == 0):
										pi[y*width] = width * 2
									else:
										pi[y*width+x] = width - y
			if index == 2 or index == 3:
				pi = [(length+1) - i for i in range(1,length+1)]
			if index == 4 or index == 5:
				pi = [0] * length
				weight = length
				for i in range(width-1):
					j = 0
					while pi[j] != 0:
						j += 1
					k = 0
					while k < width-i:
						pi[j] = weight
						j += 1
						weight -= 1
						k += 1
					j += i
					pi[j] = weight
					weight -= 1
					j += width
					while j < length - 1 :
						pi[j] = weight
						weight -= 1
						j += width
			if index == 6:
				pi = [1] * length
				rho = 1 / ((width - 3) + 1)
			if index == 7:
				pass
			if index == 8:
				mid = floor(length/2)
				for i in range(0,mid):
					pi[i] = mid - i
				if length % 2 == 1:
					pi[mid] = length
					mid += 1
				for i in range(mid,length):
					pi[i] = i+1
				rho = 2.5
			if index == 9:
				rho = 2
				j = 1
				for i in range(0,length):
					pi[i] = abs(floor(length/2) - (floor((j-1)/2)))
					if i < length-1:
						i += 1
						pi[i] = abs(floor(length/2) - (floor((j-1)/2)))
					j+=1
				if length % 2 == 1:
					pi[length-1] = 1
				shuffle(pi)
			weightings.append((pi,rho,index))
		return weightings
	def correct(self):
		for move in self.moves:
			move.inv,move.dis,move.man,move.h = move.details()
			move.f = move.g + move.h
			move.moves = move.findMoves( True )
	@staticmethod
	def inArray(taquin,array):
		for element in array:
			if element.sequence == taquin.sequence:
				return True
		return False
	def aStar(self):
		print(self.moves[-1])

		explored = dict()
		queue = OrderedDict()
		queue[self.moves[-1].f] = [self.moves[-1]]

		while (True):
			k = list(queue.keys())[0]
			shouldBeExpanded = queue[k][0]
			del queue[k][0]

			explored[str(shouldBeExpanded.sequence)] = shouldBeExpanded

			if queue[k] == []:
				del queue[k]

			children = shouldBeExpanded.children()
			if isinstance(children,Taquin):
				print(children)
				self.end.append(children)
				return self.end[-1]
			else:
				for child in children :
					sequenceString = str(child.sequence)
					if(sequenceString in explored):
						if(explored[sequenceString].f<child.f):
							del child
						else: del explored[sequenceString]
					elif(child.f in queue):
						queue[child.f].append(child)
					else:
						queue[child.f] = [child]
				queue = OrderedDict( sorted( queue.items(), key=lambda t: t[0]))

	def idaStar(self):
		root = self.moves[-1]
		print(root)
		bound = root.h
		path = [root]
		Infinity = 10000000000
		def search(path,g,bound):
			node = path[-1]
			f = g + node.h
			if f > bound: return f
			minimum = Infinity
			children = node.children()
			if isinstance(children,Taquin):
				path.append(children)
				return children
			else:
				for child in children:
					if not child.environment.inArray(child,path):
						path.append(child)
						t = search(path,g+1,bound)
						if isinstance(t,Taquin): return t
						if t < minimum: minimum = t
						path.pop()
			return minimum
		while (True):
			t = search(path,0,bound)
			if isinstance(t,Taquin):
				print(t)
				self.end.append(t)
				return t
			if t == Infinity: return False
			bound = t


	def expand(self,function,decomposition=0):
		if (decomposition==0):
			self.createdTaquins = 1
			print("\n\n")
			start = time.time()
			print(("Heuristiques utilisées : {}").format(self.choices))
			result = function()
			print(("Duration : {}").format(time.time() - start))
			print("\n\n")
			return result
		else:
			results = []
			decomposition = self.weightings.copy()
			for weighting in decomposition:
				self.createdTaquins = 1
				print("\n")
				start = time.time()
				print(("Heuristiques utilisées : {}").format(weighting[2]))
				self.weightings = [weighting]
				self.correct()
				results.append(function())
				print(("Duration : {}").format(time.time() - start))
				print("\n\n.........................................\n")
			return results



	def play(self,move):
		self.moves.append(Taquin(self,self.moves[-1],move))
		return self.moves[-1]





class __main__:
	width = int(input(">>> Taille du taquin ?\n>>> "))
	choices = str(input(">>> Heuristiques ?\n>>> Entrez les numéros séparés par des espaces.\n>>> "))
	decomposition = 0
	if len(choices) == 1: choices = [int(choices)]
	else:
		choices = choices.split(' ')
		for index,choice in enumerate(choices): choices[index] = int(choice)
		decomposition = int(input(">>> Voulez-vous associer les heuristiques [0] ou dissocier les exécutions [1] ?\n>>> "))
	a = Environment(width,choices)
	"""while(a.moves[-1].h != 0):
		move = "_"
		while not move in ["R","L","D","U","E"]:
			move = str(input((">>> Dans quel direction voulez vous aller ? {}\n>>> Ou alors peut-être voulez-vous explorer ? ['E']\n>>> ").format(a.moves[-1].moves)))
		if move in a.moves[-1].moves:
			a.play(move)
		elif move == "E":"""
	#a.expand(a.aStar,decomposition)
	a.expand(a.idaStar,decomposition)
	exit(0)