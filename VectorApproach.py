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
        self.green = ["_"]*5
        self.yellow = []
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
                if ch in self.yellow:
                    self.yellow.remove(ch)
                self.green[index] = ch
                letter = ord(ch)
                indexOfLetter = letter - 97
                self.location[(26*index):(26*(index+1))] = -1 #We know the index is nothing but the letter we just found, set it all to -1
                self.location[indexOfLetter + (26*index)] =1
                indexes = np.arange(5) * 26
                indexes+=indexOfLetter
                for ind in indexes:
                    if self.location[ind] == 0.5: #reset any yellows
                        self.location[ind] = 0.0
            index += 1

    def addYellows(self, yellowSTR: str):
        #print("Adding yellows")
        index = 0
        for ch in yellowSTR:
            if ch == "_":
                #print("blank")
                pass
            else:
                if ch not in self.yellow:
                    self.yellow.append(ch)
                    #print(self.yellow)
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
        #print("Adding grey")
        if greys != ['']:    
            for i in greys:
                if i not in  self.grey:
                    self.grey.append(i)
            #print(self.grey)
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
                        elif self.location[i] > 0:
                            pass
                        else:
                            self.location[i] = -1
                    #np.put(self.location, indexes, [-1,-1,-1,-1,-1])
            #print(self.location)
        else:
            print("Empty Greys")
            
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
    guessVec: The current guess and the info it holds
    rWords: remaining words list
    '''
    guessLoc = guessVec.location
    listoWords = []
    isSort = False
    for word in rWords:
        skip = False
        #print("Testing Word: " + word.word)
        
        for i in range(len(guessVec.green)):
            if guessVec.green[i]!= "_" and guessVec.green[i] != word.word[i]:
                #print(word.word + " deleted for lack green")
                rWords.remove(word)
                skip=True
                break
        if not skip:
            for c in guessVec.yellow:
                #print("char? " + c)
                if c not in word.word:
                    #print(word.word + " deleted for lack yellow")
                    rWords.remove(word)
                    skip=True
                    break
        if not skip:
            if guessVec.grey != ['']:
                for c in guessVec.grey:
                    if c in word.word:
                        if c not in guessVec.green: 
                            if c not in guessVec.yellow:
                                print(word.word + " deleted for grey: " + c)
                                print("Yellow: " + str(guessVec.yellow))
                                print("Green: " + str(guessVec.green))
                                rWords.remove(word)
                                skip=True
                                break
        #print("rwords: " + str(len(rWords)))
        if skip:
            #print("skpping")
            pass
        else:
            #print("ELSE HAPPENED")
            testingword = word
            dist = eucDist(guessVec, testingword)
            if len(listoWords) <11:
                listoWords.append([dist, word.word])
                #print("list still short")
                if len(listoWords) ==11:
                    listoWords.sort(key= lambda lit: lit[0],reverse=False)
                    isSort = True
            else:
                for i in range(len(listoWords)):
                    if dist <= listoWords[i][0]:
                        listoWords[i] = [dist, word.word]
                        #print("long but adding Adding to top 10:" + word.word)
                        break
    if not isSort:
        listoWords.sort(key= lambda lit: lit[0],reverse=False)
    return([listoWords, rWords])


if __name__ == "__main__":
    print("Initalizing Word List.")
    #Open provided file, get word from each line, append to list of all words, close file.
    unsortedWords= []
    file = open(ValidWordsPath)
    for line in file:
        #unsortedWords.append(line.strip())
        unsortedWords.append(IIVectorizedWord(str(line.strip()).lower()))
    file.close()
    print("Added " + str(len(unsortedWords)) + " words to list." )


    print("-=#Vector Based Wordle Guess Maker#=-")
    
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
        guessGREEN = input("Enter the known letters, unknown letters as an _: ").lower().strip()
        guessYELLLOW = input("Enter the yellows, unknown letters as an _: ").lower().strip()
        print("if a letter is green do not add it to greys incase of repeat")
        guessGREY = input("Enter NEW greys, space seperated: ").strip().split(" ")

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
        
        
