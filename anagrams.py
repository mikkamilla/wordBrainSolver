

class Anagrams():
    def __init__(self):
        pass

    def getWordSet(self):
        wordlist = (line.strip() for line in open('words_alpha.txt'))
        #wordset = set([ parola[:3] for parola in wordlist if len(parola) >=3 ])
        wordset = set(wordlist)
        return wordset



if __name__ == "__main__":


    test = Anagrams()
    print test.getWordSet()