import nltk
import enchant
import numpy as np
import sys


class WordBrainSolver():

	def __init__(self, array, wordLength):
		self.x = np.array(array, dtype=str)
		self.matrix = self.x.view('S1').reshape((self.x.size, -1))
		self.wordLength = wordLength
		(self.rows, self.columns) = self.matrix.shape
		self.graph = {}

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
		for item in self.graph:
			print item, self.graph[item]

	def findAllPathsAsLongAS(self, start, path=[]):
		path = path + [start]
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
		return paths

	def translate(self, combinations):
		for combination in combinations:
			word = ''
			for tupla in combination:
				word += self.matrix[tupla]
			if self.isAValidWord(word):
				print word

	def isAValidWord(self, word):
		d = enchant.Dict("en_US")
		return d.check(word)

	def main(self):
		self.printMatrix()
		self.createGraph()
		print 50 * "-"
		print "PATHS"
		print('Looking only for {0} letters words'.format(self.wordLength))
		print 50 * "-"
		for i in range(self.rows):	
			for j in range(self.columns):
				#print self.findAllPathsAsLongAS((i,j))
				if self.matrix[(i,j)].isalpha():
					print "start point: ", (i,j), "->", self.matrix[(i,j)]
					self.translate(self.findAllPathsAsLongAS((i,j)))

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
	#array = ['abc', 'def','ghi']
	#array = ['ama','tsr','ard']
	#array = ['abcd','efgh','ijkl', 'mnop']
	#array = ['nvne','aytm','cgin', 'eren', 'nroe']
	array = ['etprf', 'lecar', 'haura', 'gnsbc', 'irtes']
	test = WordBrainSolver(array, 8)
	test.main()
	#test.getAnagrams('citapls')
