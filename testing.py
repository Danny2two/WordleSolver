letterarr = [[]]*26
#print(letterarr)

str = "abcdefghijklmnopqrstuvwxyz"
for letter in str.encode('ascii'):
    print(letter-97)