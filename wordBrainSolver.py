#import nltk
#from nltk.corpus import words
#import enchant
import numpy as np
import sys


class WordBrainSolver():

	def __init__(self, array, wordLengths):
		x = np.array(array, dtype=str)
		self.matrix = x.view('S1').reshape((x.size, -1))
		self.wordLengths = wordLengths
		(self.rows, self.columns) = self.matrix.shape

		sum = 0
		try:
			for num in wordLengths:
				sum += num
		except TypeError: 
			sys.exit("check syntax, you need wordLengths to be a tuple of numbers")
		if  not (sum == (self.rows * self.columns)):
			sys.exit("check word lenghts you provided")

		self.graph = {}
		#self.wordlist = (line.strip() for line in open('words_alpha.txt'))
		
	def printMatrix(self):
		print 50 * "-"
		print "MATRIX"
		print 50 * "-"
		print("dimensions: {0}x{1}".format(str(self.rows), str(self.columns)))
		print self.matrix

	def getExtremes(self, index, rowOrCol):
		#rowOrCol can be 'row' or 'col'
		dimension = self.rows - 1 if rowOrCol == 'row' else self.columns - 1
		return (0 if index == 0 else index - 1, dimension if index == dimension else index + 1)

	def getWordSet(self):
		return self.wordset

	def findNeighbors(self, i, j):
		(minRow, maxRow) = self.getExtremes(i, 'row')
		(minCol, maxCol) = self.getExtremes(j, 'col')
		neighbors = []	
		for m in range (minRow, maxRow+1):
			for n in range (minCol, maxCol+1):	
				if (i, j) != (m, n):
					neighbors.append((m,n))
		return neighbors

	def createGraph(self):
		print 50 * "-"
		print "GRAPH"
		print 50 * "-"
		for i in range(self.rows):	
			for j in range(self.columns):
				root = (i,j)
				self.graph[root] = self.findNeighbors(i, j)

	def printGraph(self):
		for item in self.graph:
			print item, self.graph[item]

	def findAllPathsAsLongAS(self, start, path=[]):
		path = path + [start]
		if len(path) >= 2:
			#print("Path: {0}".format(path))
			parola = ''
			for tupla in path:
				parola += self.matrix[tupla]
			print("Parola: {0}, len: {1}".format(parola, len(parola)))
			if parola not in set([ parola[:len(path)] for parola in (line.strip() for line in open('words_alpha.txt')) if len(parola) >= len(path) ]):
				print("{0} proprio non ci sta".format(parola))
				return []
		if len(path) == self.wordLength:
			return [path]
		if not self.graph.has_key(start):
			return []
		paths = []
		for node in self.graph[start]:
			if node not in path and self.matrix[node].isalpha():
				newpaths = self.findAllPathsAsLongAS(node, path)
				for newpath in newpaths:
					paths.append(newpath)
		#print paths
		return paths

	def translate(self, combinations):
		for combination in combinations:
			print("Combination: {0}".format(combination))
			word = ''
			for tupla in combination:
				word += self.matrix[tupla]

			if self.isAValidWord(word):
				#print "###################"
				print("###################Valid english word: {0}".format(word))
				#print "###################"
			#else: print("NON valid english word: {0}".format(word))


	def isAValidWord(self, word):
		d = enchant.Dict("en_US")
		return d.check(word)

	def temp(self):
		"would" in words.words()

	def main(self):
		self.printMatrix()
		self.createGraph()
		self.printGraph()
		#print 50 * "-"
		#print "PATHS"
		#print('Looking only for {0} letters words'.format(self.wordLength))
		#print 50 * "-"
		#for i in range(self.rows):	
		#	for j in range(self.columns):
		#		if self.matrix[(i,j)].isalpha():
		#			print "start point: ", (i,j), "->", self.matrix[(i,j)]
		#			self.translate(self.findAllPathsAsLongAS((i,j)))

	def getAnagrams(self, jumbled_letters):
		all_words = nltk.corpus.words.words()
		#print len(all_words), "total words loaded" 

		letter_distribution = nltk.FreqDist(jumbled_letters) 
		matching_wordlist = [w.lower() for w in all_words if nltk.FreqDist(w) <= letter_distribution]

		print "found: " + str(len(matching_wordlist)) + " matching words"
		print "but only these are long " + str(self.wordLength) + " characters:"
	
		matches = []
		for parola in matching_wordlist:
			if len(parola) == self.wordLength:
				matches.append(parola)
		lmatches = set(matches)
		print len(lmatches)
		print matches


if __name__ == "__main__":
	#array = ['ab', 'cd']

	array = [	'asx', 
				'rwy',
				'eax']

	#array = ['ama','tsr','ard']
	#array = ['dks','oah','pro', 'arp']
	#array = ['nvne','aytm','cgin', 'eren', 'nroe']
	"""
	array = [	'etpr', 
				'leca', 
				'haur', 
				'gnsb', 
				'irte']
	"""
	test = WordBrainSolver(array, (4,3,2))
	test.main()
	#print len(test.getWordSet())
	#test.getAnagrams('citapls')
