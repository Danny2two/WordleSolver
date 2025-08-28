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
        self.location = np.ones((26 * 5,1))
        self.location *= -1
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
    def __init__(self,word:str,yellow:str,grey: list[str]):
        '''
        word: known good letters in their spot ie "BO__Y"
        yellow: yellow letters in their spot ie "__GG_"
        grey: list of known false letters ie [X, Z, U]
        '''
        self.location = np.zeros((26 * 5,1)) #will be venctor of known good "starting point"
        self.yellow = yellow
        self.grey = grey
        index = 0
        for ch in word:
            if ch == "_":
                print("blank")
                #pass
            else:
                letter = ord(ch)
                indexOfLetter = letter - 97
                self.location[(26*index):(26*(index+1))] = -1
                self.location[indexOfLetter + (26*index)] =1
            index += 1
        self.addYellows(yellow)
        self.addGrey(grey)

    def addYellows(self, yellowSTR: str):
        print("Adding yellows")
        index = 0
        for ch in yellowSTR:
            if ch == "_":
                print("blank")
                #pass
            else:
                letter = ord(ch)
                indexOfLetter = letter - 97
                self.location[indexOfLetter + (26*index)] =-1
                indexes = np.arange(5) * 26
                indexes+=indexOfLetter
                for ind in indexes:
                    if self.location[ind] == 0:
                        self.location[ind] = 0.5
                        
            index += 1
        print(str(self.location))

    def addGrey(self, greys: list[str]):
        print("Adding grey")
        self.grey+= greys
        for str in greys:
            ch = str[0]
            if ch == "_":
                print("blank")
                #pass
            else:
                letter = ord(ch)
                indexOfLetter = letter - 97
                indexes = np.arange(5) * 26
                indexes+=indexOfLetter
                np.put(self.location, indexes, [-1,-1,-1,-1,-1])
        #print(self.location)
            
    def get_loc(self):
        return self.location
    
    def __str__(self):
        str1 = str(self.location[0:26]).replace("\n", "")
        str2 = str(self.location[26:(26*2) ]).replace("\n", "")
        str3 = str(self.location[(26*2) :(26*3) ]).replace("\n", "")
        str4 = str(self.location[(26*3) :(26*4) ]).replace("\n", "")
        str5 = str(self.location[(26*4) :(26*5) ]).replace("\n", "")
        return "Slot 1: " + str1 + "\nSlot 2: " + str2 + "\nSlot 3: " + str3 +"\nSlot 4: " + str4 +"\nSlot 5: " + str5
        

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

#word1 = IIVectorizedWord("boaty")
#print(word1.get_loc())

guess1 = IIVectorizedGuess("__a_t","s____", ["u","d","i",'o','l','p','h','w','y','k'])#print(guess1.get_loc())
print(str(guess1))

listoWords = [[]]*10
index = -1
for word in unsortedWords:
    index += 1
    #print("Testing Word: " + word)
    testingword = IIVectorizedWord(word)
    dist = eucDist(guess1, testingword)
    if index <10:
        listoWords[index] = [dist, word]
    else:
        for i in range(len(listoWords)):
            if dist <= listoWords[i][0]:
                listoWords[i] = [dist, word]
                #print("Adding to top 10:" + word)
                break
print(str(listoWords))
