import numpy as np
#Path to words list
ValidWordsPath= './valid_wordle_words.txt'

class VectorizedWord:
    def __init__(self,word: str):
        self.location = np.zeros((26 *5, 1))

    def get_loc(self):
        return self.location
    
class IIVectorizedWord(VectorizedWord):
    def __init__(self,word:str):
        """Vector representation of a 5 letter string in 130d vector space

        Args:
            word (str): 5 letter string used to generate vector 
        """
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
        """Returns the vector pointing to this word in vector space

        Returns:
            ndarray: 130x1 vector encoding the location of the word
        """
        return self.location

    def __str__(self):
        str1 = str(self.location[0:26]).replace("\n", "")
        str2 = str(self.location[26:(26*2) ]).replace("\n", "")
        str3 = str(self.location[(26*2) :(26*3) ]).replace("\n", "")
        str4 = str(self.location[(26*3) :(26*4) ]).replace("\n", "")
        str5 = str(self.location[(26*4) :(26*5) ]).replace("\n", "")
        return "Slot 1: " + str1 + "\nSlot 2: " + str2 + "\nSlot 3: " + str3 +"\nSlot 4: " + str4 +"\nSlot 5: " + str5
        
class IIVectorizedGuess(VectorizedWord):
    def __init__(self,word:str,yellow:str,grey: list[str]):
        """Vector representation of a guess, continually updated with new information

        Args:
            word (str): 5 letter string of KNOWN letters ie the green results from wordle. Fill in unknown letters with an underscore.
            yellow (str): 5 letter string of yellow letters from wordle. Fill in unknown letters with an underscore.
            grey (list[str]): list of strings, each string being a known grey result from wordle. 
        """
        self.location = np.zeros((26 * 5,1))
        self.green = ["_"]*5
        self.yellow = []
        self.grey = grey
        self.addGreens(word)
        self.addYellows(yellow)
        self.addGrey(grey)

    def addGreens(self,greenSTR: str):
        """Adds known values to this words vector. 

        Args:
            greenSTR (str): 5 letter string of KNOWN letters ie the green results from wordle. Fill in unknown letters with an underscore.
        """
        index = 0
        for ch in str(greenSTR):
            if ch == "_":
                #print("blank")
                pass
            else:
                if ch in self.yellow:
                    self.yellow.remove(ch)
                self.green[index] = ch
                indexOfLetter = get_letter_index(ch)
                self.location[(26*index):(26*(index+1))] = -1 #We know the index is nothing but the letter we just found, set it all to -1
                self.location[indexOfLetter + (26*index)] =1 #Set correct dimension to 1
                indexes = np.arange(5) * 26
                indexes+=indexOfLetter
                for ind in indexes:
                    if self.location[ind] == 0.5: #reset any yellows
                        self.location[ind] = 0.0
            index += 1

    def addYellows(self, yellowSTR: str):
        """Adds yellow letters to this words vector

        Args:
            yellowSTR (str): 5 letter string of yellow letters from wordle. Fill in unknown letters with an underscore.
        """
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
                indexOfLetter = get_letter_index(ch)
                self.location[indexOfLetter + (26*index)] =-1 #Set dimension where yellow was found to -1, we know this letter is not here
                indexes = np.arange(5) * 26
                indexes+=indexOfLetter
                for ind in indexes:
                    if self.location[ind] == 0: #If the dimension is 0 we know its not already been set by a green or grey
                        self.location[ind] = 0.5
                        
            index += 1
        #print(str(self.location))

    def addGrey(self, greys: list[str]):
        """Adds known grey values to this words vector

        Args:
            greys (list[str]): List of strings containing the grey letters to be added
        """
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
                    indexOfLetter = get_letter_index(ch)
                    indexes = np.arange(5) * 26
                    indexes+=indexOfLetter
                    for i in indexes:
                        #print(i)
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
        """Returns the vector pointing to this word in vector space

        Returns:
            ndarray: 130x1 vector encoding the location of the word
        """
        return self.location
    
    def __str__(self):
        str1 = str(self.location[0:26]).replace("\n", "")
        str2 = str(self.location[26:(26*2) ]).replace("\n", "")
        str3 = str(self.location[(26*2) :(26*3) ]).replace("\n", "")
        str4 = str(self.location[(26*3) :(26*4) ]).replace("\n", "")
        str5 = str(self.location[(26*4) :(26*5) ]).replace("\n", "")
        return "Slot 1: " + str1 + "\nSlot 2: " + str2 + "\nSlot 3: " + str3 +"\nSlot 4: " + str4 +"\nSlot 5: " + str5
        
def get_letter_index(ch:chr):
    """Returns the index of a letter

    Args:
        ch (char): Character to get index of

    Returns:
        int: index of letter in alphabet.
    """
    letter = ord(ch)
    indexOfLetter = int(letter - 97)
    return indexOfLetter

def eucDist(VecWord: VectorizedWord, VecWord2: VectorizedWord):
    dist = 0
    for i in range(26 * 5):
        dist += np.pow((VecWord.location[i] - VecWord2.location[i]),2)
    return np.sqrt(dist)

def guessMaker(guessVec: IIVectorizedGuess, rWords: list[IIVectorizedWord]):
    """Ranks the remaining words against the guess to determine the next closest valid guesses. Eliminates impossible words from the search list entirely. 

    Args:
        guessVec (IIVectorizedGuess): current guess
        rWords (list[IIVectorizedWord]): List of remaining words.

    Returns:
        list[list[],list[]]: A list consisting of two elements, [0] being the ranked list of possible guesses; [1] being the remaining word list.
    """
    guessLoc = guessVec.location
    listoWords = []
    isSort = False
    for word in rWords:
        if np.allclose(guessLoc,word.get_loc(),atol=1.5, rtol=0 ):
            #print("Allclose with word: " + word.word)
            #print(str(guessVec) + "\n" + str(word))
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
        else:
            #print("Not all close")
            pass
    if not isSort:
        listoWords.sort(key= lambda lit: lit[0],reverse=False)
    return([listoWords, rWords])


if __name__ == "__main__":
    print("Initalizing Word List.")
    #Open provided file, get word from each line, append to list of all words, close file.
    unsortedWords= []
    try:
        file = open(ValidWordsPath)
    except FileNotFoundError:
        print("Invalid File location for word list")
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
        
        
