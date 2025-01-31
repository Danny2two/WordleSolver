#Parse List
#Path to words list
ValidWordsPath= './valid_wordle_words.txt'

#Open provided file, get word from each line, append to list of all words, close file.
unsortedWords= []
file = open(ValidWordsPath)
for line in file:
    unsortedWords.append(line.strip())
file.close()
#print(unsortedWords)

#Create list of list for each letter
letterarr = [[] for i in range(0, 26)]
double_letterarr = [[] for i in range(0, 26)]

for word in unsortedWords:
    print(word)
    alr_appended = []
    for ch in word:
        letter = ord(ch)
        indexOfLetter = letter - 97
        Cur_letter_arr = letterarr[indexOfLetter]
        Cur_D_letter_arr = double_letterarr[indexOfLetter]

        if indexOfLetter in alr_appended:
            #print("Appending " + word + " DOUBLE list " + str(indexOfLetter) + " (" + chr(letter) + ")")
            Cur_D_letter_arr.append(word)
        else:
            #print("Appending " + word + " list " + str(indexOfLetter) + " (" + chr(letter) + ")")
            Cur_letter_arr.append(word)
            alr_appended.append(indexOfLetter)

subset0 = []
for word in letterarr[0]:
    if word[0] == 'a':
        subset0.append(word)
print(subset0)

subset1 = []
for word in subset0:
    if  word[1] == 'm':
        subset1.append(word)
print(subset1)

subset2 = []
for word in subset1:
    if  word[2] == 'm':
        subset2.append(word)
print(subset2)

subset3 = []
for word in subset2:
    if  word[3] == 'o':
        subset3.append(word)
print(subset3)