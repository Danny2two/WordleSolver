import numpy as np
#Parse List
#Path to words list
ValidWordsPath= './valid_wordle_words.txt'

green = 1
yellow = 0.5

#Open provided file, get word from each line, append to list of all words, close file.
unsortedWords= []
file = open(ValidWordsPath)
for line in file:
    unsortedWords.append(line.strip())
file.close()
#print(unsortedWords)

class VectorizedWord:
    def __init__(self,word):
        self.location = np.zeros((26,5))

    def get_loc(self):
        return self.location

class IVectorizedWord(VectorizedWord):
    def __init__(self,word):
        self.location = np.zeros((26,5))
        index = 0
        for ch in word:
            letter = ord(ch)
            indexOfLetter = letter - 97
            self.location[indexOfLetter][index] = 1
            index += 1
        pass

    def get_loc(self):
        return self.location
    
class IIVectorizedWord(VectorizedWord):
    def __init__(self,word):
        self.location = np.zeros((26 * 5,1))
        index = 0
        for ch in word:
            letter = ord(ch)
            indexOfLetter = letter - 97
            self.location[indexOfLetter + (26*index)] =1
            index += 1
        pass

    def get_loc(self):
        return self.location
    
class IIVectorizedGuess(VectorizedWord):
    def __init__(self,word,yellow,grey):
        '''
        word: known good letters in their spot ie "B O _ _ Y"
        yellow: yellow letters in their spot ie "_ _ G G _"
        grey: list of known false letters ie [X, Z, U]
        '''
        self.location = np.zeros((26 * 5,1)) #will be venctor of known good "starting point"
        self.yellow = yellow
        self.grey = grey
        index = 0
        for ch in word:
            if ch == " " or "_":
                print("blank")
            else:
                letter = ord(ch)
                indexOfLetter = letter - 97
                self.location[indexOfLetter + (26*index)] =1
            index += 1
        pass

    def get_loc(self):
        return self.location

def eucDist(VecWord: IIVectorizedWord, VecWord2: IIVectorizedWord):
    dist = 0
    for i in range(26 * 5):
        dist += np.pow((VecWord.location[i] - VecWord2.location[i]),2)
    return np.sqrt(dist)

def guessMaker(guessVec: IIVectorizedGuess, rWords):
    '''
    Places the yellow in possible spots and sees whats near by in the vector space
    guessVec: The current guess and the info it holds
    rWords: remaining words list
    '''

word1 = IIVectorizedWord("boaty")
print(word1.get_loc())

guess1 = IIVectorizedGuess("bo   ","__t__", ["z","k","i"])
print(guess1.get_loc())

"""
listoWords = [[]]*10
index = -1
for word in unsortedWords:
    index += 1
    print("Testing Word: " + word)
    testingword = IIVectorizedWord(word)
    dist = eucDist(word1, testingword)
    if index <10:
        listoWords[index] = [dist, word]
    else:
        for i in range(len(listoWords)):
            if dist <= listoWords[i][0]:
                listoWords[i] = [dist, word]
                print("Adding to top 10:" + word)
                break
print(str(listoWords))"""