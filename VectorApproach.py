import numpy as np
#Parse List
#Path to words list
ValidWordsPath= './valid_wordle_words.txt'

green = 1
yellow = 0.5

class VectorizedWord:
    def __init__(self,word: str):
        self.location = np.zeros((26,5))

    def get_loc(self):
        return self.location

class IVectorizedWord(VectorizedWord):
    def __init__(self,word: str):
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
        self.word=word
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
        self.green = word
        self.yellow = yellow
        self.grey = grey
        self.addGreens(word)
        self.addYellows(yellow)
        self.addGrey(grey)

    def addGreens(self,greenSTR: str):
        index = 0
        for ch in str(greenSTR):
            if ch == "_":
                #print("blank")
                pass
            else:
                letter = ord(ch)
                indexOfLetter = letter - 97
                self.location[(26*index):(26*(index+1))] = -1 #We know the index is nothing but the letter we just found, set it all to -1
                self.location[indexOfLetter + (26*index)] =1
                indexes = np.arange(5) * 26
                indexes+=indexOfLetter
                for ind in indexes:
                    if self.location[ind] == 0.5:
                        self.location[ind] = 0
            index += 1

    def addYellows(self, yellowSTR: str):
        print("Adding yellows")
        index = 0
        for ch in yellowSTR:
            if ch == "_":
                #print("blank")
                pass
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
        #print(str(self.location))

    def addGrey(self, greys: list[str]):
        print("Adding grey")
        self.grey+= greys
        print(self.grey)
        for stri in self.grey:
            ch = stri[0]
            if ch == "_":
                #print("blank")
                pass
            else:
                letter = ord(ch)
                indexOfLetter = letter - 97
                indexes = np.arange(5) * 26
                indexes+=indexOfLetter
                for i in indexes:
                    print(i)
                    if self.location[i] ==1:
                        pass
                    if self.location[i] > 0:
                        pass
                    else:
                        self.location[i] = -1
                #np.put(self.location, indexes, [-1,-1,-1,-1,-1])
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
        

def eucDist(VecWord: VectorizedWord, VecWord2: VectorizedWord):
    dist = 0
    for i in range(26 * 5):
        dist += np.pow((VecWord.location[i] - VecWord2.location[i]),2)
    return np.sqrt(dist)

def guessMaker(guessVec: IIVectorizedGuess, rWords: list[IIVectorizedWord]):
    '''
    Places the yellow in possible spots and sees whats near by in the vector space
    guessVec: The current guess and the info it holds
    rWords: remaining words list
    '''
    guessLoc = guessVec.location
    listoWords = []
    index = -1
    for word in rWords:
        skip = False
        index += 1
        #print("Testing Word: " + word)
        '''
        for c in guessVec.grey: #if the word has a grey letter,
            #print(c)
            if c in word.word and c not in guessVec.green:
                #print(word + " deleted")
                if word.word.find(c) != guessVec.green.find(c):
                    del rWords[index]
                    index -=1 
                    skip=True
                    break
                    '''
        for i in range(len(guessLoc)): #this needs work
            if abs(guessLoc[i] - word.location[i]) >=2  :
                print(word.word + " deleted")
                del rWords[index]
                index -=1 
                skip=True
                break


        if skip:
            #print("skpping")
            pass
        else:
            testingword = word
            dist = eucDist(guessVec, testingword)
            if len(listoWords) <10:
                listoWords.append([dist, word.word])
            else:
                for i in range(len(listoWords)):
                    if dist <= listoWords[i][0]:
                        listoWords[i] = [dist, word.word]
                        #print("Adding to top 10:" + word)
                        break
    return([listoWords, rWords])


if __name__ == "__main__":
    print("Initalizing Word List")

    #Open provided file, get word from each line, append to list of all words, close file.
    unsortedWords= []
    file = open(ValidWordsPath)
    for line in file:
        #unsortedWords.append(line.strip())
        unsortedWords.append(IIVectorizedWord(str(line.strip()).lower()))
    file.close()
    #print(unsortedWords)


    print("Vector Based Wordle Guess Maker")
    
    guessGREEN = input("Enter the known letters, unknown letters as an _: ").lower()
    guessYELLLOW = input("Enter the yellows, unknown letters as an _: ").lower()
    print("if a letter is green do not add it to greys incase of repeat")
    guessGREY = input("Enter the greys, space seperated: ").split(" ")

    #print(guessGREEN)

    guessInit = IIVectorizedGuess(guessGREEN,guessYELLLOW,guessGREY)
    results = guessMaker(guessInit,unsortedWords)
    print(results[0])
    print(guessInit)

    remainingWords = results[1]
    input("Enter to continue")
    cont = True
    while cont:
        guessGREEN = input("Enter the known letters, unknown letters as an _: ").lower()
        guessYELLLOW = input("Enter the yellows, unknown letters as an _: ").lower()
        print("if a letter is green do not add it to greys incase of repeat")
        guessGREY = input("Enter NEW greys, space seperated: ").split(" ")

        guessInit.addGreens(guessGREEN)
        guessInit.addYellows(guessYELLLOW)
        guessInit.addGrey(guessGREY)

        results = guessMaker(guessInit,unsortedWords)
        print(results[0])
        print("With greys: " + str(guessInit.grey))
        print(guessInit)
        remainingWords = results[1]

        if(input("Enter to continue, Q to exit: ").lower() == "q"):
            cont = False
        
        
