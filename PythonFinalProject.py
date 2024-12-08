#!/usr/bin/env python
# coding: utf-8

# In[10]:


'''
Barnabas Abekorode 100874494
Bernard Yeboah 100861980
Pavi Vijeyarajah 100874494
March 4, 2023

The purpose of this program is to allow the user to type messages
and get the plaintext, encryption, and type of encrytion of those
messages after entering them. The ciphers that are used to encrypt
the user's text is: Transposition, Playfair, Subsitution, Ceaser, 
Product, and RSA.
'''
import random
import string
import math

class Message():
    '''
    This initializer method takes the words from the user
    @param self,word for holding the holding the words user inputted
    @return N/A
    '''
    def __init__(self,word=[]):
        self.words=word
    '''
    This mutator method allows the class to access the user input
    @param self,word from the user that is added to the word list
    @return N/A
    '''    
    def set_words(self,word):
        self.words.append(word)
    '''
    This method assignes a number to each of the words the user inputs to find which cipher to encrypt it
    @param self
    @return 1,2,3,4,5,6 returned to represent a cipher that is chosen at random
    '''
    def assignCipher(self):
        for i in range(len(self.words)):
            select=random.randint(1,6)
            if select==1:
                return 1
            if select==2:
                return 2
            if select==3:
                return 3
            if select==4:
                return 4
            if select==5:
                return 5
            if select==6:
                return 6
            
'''
This class is an inheritance class that is the parent for all the encryptions for the ciphers
'''
class Encryption(object):
    '''
    This initializer method holds values that are similar in all of the class initializers for encryption ciphers
    @param self,key holds the key used to encrypt,msg holds the message given by the user
    @return N/A
    '''
    def __init__(self,key,msg=""):
        pass
    '''
    This mutator method is an overriding method for setting the message
    @param self,msg allows user message to be used in the class
    @return N/A
    '''
    def set_msg(self,msg):
        pass
    '''
    This encryption method is an overriding method for the encrypting the message
    @param self
    @return encryption this reuturns the message that was encrypted
    '''
    def encrypt(self):
        return encryption


class TranspositionEncryption(Encryption):
    '''
    This initializer method holds key which is the method of encrypting and the message
    @param self,key holds the key used to encrypt,msg holds the message given by the user
    @return N/A
    '''
    def __init__(self, key,msg=''):
        self.key = key
        self.msg = msg
    '''
    This mutator method is an overriding method for setting the message
    @param self,msg allows user message to be used in the class
    @return N/A
    '''
    def set_msg(self,msg):
        self.msg=msg
    '''
    This encryption method is an overriding method for the encrypting the message using a number of columns based on the key
    @param self
    @return encryption this reuturns the message that was encrypted
    '''
    def encrypt(self):    # Add to the message to fit the matrix
        num_fill_chars = len(self.key) - (len(self.msg) % len(self.key))
        message_list = list(self.msg.ljust(len(self.msg) + num_fill_chars, "*"))

        # Create the matrix
        matrix = [[message_list[i + j] for j in range(len(self.key))] for i in
                  range(0, len(message_list), len(self.key))]

        # Read the matrix in terms of the column using the key
        cipher = "".join("".join(row[self.key.index(k)] for row in matrix) for k in sorted(self.key))

        return cipher
    
    
class PlayfairEncryption(Encryption):
    '''
    This initializer method holds key which is the method of encrypting, the message from the user, and the modified pairs used for the rules
    @param self,key holds the key used to encrypt,msg holds the message given by the user, mod_pairs used to hold changes based on the rules
    @return N/A
    '''
    def __init__(self, key,msg="",mod_pairs=[]):
        self.key = key
        self.msg=msg
        self.key_matrix = self.generate_key_matrix()  # generate the key matrix using the provided key
        self.modified_pairs=mod_pairs #initialize an empty list for the modified pairs
    '''
    This mutator method is an overriding method for setting the message
    @param self,msg allows user message to be used in the class
    @return N/A
    '''
    def set_msg(self,msg):
        self.msg=msg
    '''
    This method makes the 5x5 matrix that will be used for the rules in the further methods
    @param self
    @return key_matrix this is the 5x5 matrix
    '''
    def generate_key_matrix(self):
        a_to_z = string.ascii_lowercase.replace('j', ' ') # create a string of all the lowercase letters except for 'j'
        key_matrix = ['' ] * 5 # initialize the key matrix as a list of 5 empty strings
      # variables to keep track of the current row and column in the key matrix
        key_count= 0
        row_count = 0
      # iterate through the characters in the provided key
        for characters in self.key:
            if characters in a_to_z and characters != ' ': # if the character is a valid lowercase letter (excluding 'j')
                key_matrix[key_count] += characters # add the character to the current row in the key matrix
                a_to_z = a_to_z.replace(characters, ' ') # remove the character from the list of available characters
                row_count += 1 #increment the row count
              #if the current row is full, move onto the next row
                if row_count == 5:
                    key_count += 1
                    row_count = 0 # reset the row count
                    
        for characters in a_to_z: # fill in the remaining spaces in the key matrix with the remaining letters from a_to_z
            if characters != ' ':
                if key_count < 5 and row_count < 5:
                    key_matrix[key_count] += characters
                    row_count += 1
                    if row_count == 5:
                        key_count += 1
                        row_count = 0
        return key_matrix
    '''
    This encryption method uses a set of 4 rules explain in the further inner methods to get the message encrypted
    @param self
    @return ciphertext the final encrypted text
    '''
    def encrypt(self):
        plaintextpairs = [] # initialize an empty list for the plaintext pairs
        ciphertextpairs = []  # initialize an empty list for the ciphertext pairs
        '''
        This rule method adds an x if 2 letters in the text beside eachother are the same or there is only a single letter
        if its different just combine them as a pair
        @param N/A
        @return plaintext pairs which is the sets of 2 letters in a list that will be encrypted and combined
        '''
        def apply_rule1():
            i = 0 # index to help go through each character in plaintext string
            while i < len(self.msg):
                first_letter = self.msg[i] # assign first_letter to first letter from plaintext
                second_letter = " " # assign second_letter to second letter from plaintext
                if i + 1 == len(self.msg):  # if we go over last character of plaintext
                    second_letter = first_letter
                else:
                    second_letter = self.msg[i + 1] # second letter from plaintext
               # ensure first letter and second letter are not the same character
                if first_letter != second_letter:
                   # if first letter and second are not the same, pair them together and add them to the plaintext list
                    plaintextpairs.append(first_letter + second_letter)
                    i = i + 2
                else:
                    if first_letter == second_letter:
                       # check if the last pair in modified_pairs contains the same letter
                        if len(self.modified_pairs) > 0 and self.modified_pairs[-1][1] == first_letter:
                           # append the other letter to the last pair in modified_pairs
                            self.modified_pairs[-1] += first_letter
                            plaintextpairs.append('x' + second_letter)
                        else:
                            plaintextpairs.append(first_letter + 'x')
                        i = i + 2           
            return plaintextpairs
        '''
        This rule method checks if each of the letters in the plaintextpairs are in the same row in the key_matrix,
        if they are in the same row swap each letter one to the right if its the last letter in row then it's swapped
        with first letter
        @param plaintextpairs which is the sets of two letters in a list
        @return N/A
        '''
        def apply_rule_2(plaintextpairs):
            self.modified_pairs=[]
            for pair in plaintextpairs:
                applied_rule = False # keep track of whether rule has been applied so it will not apply the next rule
                for row in self.key_matrix:
                    if pair[0] in row and pair[1] in row:  # check if both characters are in the same row
                        j0 = row.find(pair[0]) # store the index of the first character in variable j0
                        j1 = row.find(pair[1]) # store the index of the second character in variable j1
                    # wrap around to the beginning of the row if we exceed the boundary using the modulo operator
                        ciphertextpair = row[(j0 + 1) % 5] + row[(j1 + 1) % 5] # move both characters to the right one
                        self.modified_pairs.append(ciphertextpair)
                        applied_rule = True
                if applied_rule == True: #if the second rule has been applied, move onto the next pair in row
                    continue
                else:
                    self.modified_pairs.append(pair)
        '''
        This rule method is similar to the one above but using columns and swapping letters one below if they are same
        @param plaintextpairs which are sets of 2 letters in a list
        @return self.modified_pairs which are the changes made from each rule
        '''
        def apply_rule_3(plaintextpairs):
            k=0
            for pair in plaintextpairs:
                applied_rule = False
                k+=1
                for j in range(5):
                    col = "".join(self.key_matrix[i][j] for i in range(5)) # Access the key matrix through the self object
                    if pair[0] in col and pair[1] in col:
                        i0, i1 = col.find(pair[0]), col.find(pair[1]) #Store indices of the characters in the colum
                        ciphertextpair = col[(i0 + 1) % 5] + col[(i1 + 1) % 5]
                        self.modified_pairs[k-1]=(ciphertextpair)
                        applied_rule = True
                if applied_rule == True:
                    continue
            return self.modified_pairs
        '''
        This rule method is done when the letters in the plaintext pairs aren't in the same row or column,
        they become corners of a rectangle in the key_matrix and the for each letter the letter on the
        opposite side of each of the corner letters swapped for them
        @param plaintextplairs which are sets of 2 letters in a list 
        @return N/A
        '''
        def apply_rule_4(plaintextpairs):
          # if letters are not in the same row or column, replace them with letters on the same row but in the other column of the original pair.
            k=0
            for pair in plaintextpairs:
                applied_rule = False  # initialize the variable before using it
                k+=1
              # find indices of the characters in the key_matrix
                for i in range(5):
                    if pair[0] in self.key_matrix[i]:
                        j0 = self.key_matrix[i].find(pair[0])
                        row0 = i
                    if pair[1] in self.key_matrix[i]:
                        j1 = self.key_matrix[i].find(pair[1])
                        row1 = i
                for j in range(5):
                    col = "".join(self.key_matrix[i][j] for i in range(5))
                    if pair[0] in col:
                        col0=j
                    if pair[1] in col:
                        col1=j
                if row0 != row1:
                    if col0 != col1:
                      # if characters are not in the same row, replace each letter with the letter in the same row but in the other column
                        ciphertextpair = self.key_matrix[row0][j1] + self.key_matrix[row1][j0]
                        self.modified_pairs[k-1]=(ciphertextpair)
                        applied_rule = True
                if applied_rule == True:
                    continue
        plaintextpairs = apply_rule1()
        apply_rule_2(plaintextpairs)
        apply_rule_3(plaintextpairs)
        apply_rule_4(plaintextpairs)
        ciphertext = ''.join(self.modified_pairs)
        return ciphertext
    
    
class SubsitutionEncryption(Encryption):
    '''
    This initializer method gets the key and message from the user
    @param self,key for encrypting message,msg for getting message from user
    @return N/A
    '''
    def __init__(self,key,msg=""):
        self.key = key
        self.msg = msg
        self.word2char=[] #convert words to list of characters
        self.char2ciph=[] #convert list of characters to ciphered list of characters   
    '''
    This mutator method allows the class to access the user input
    @param self,msg for getting message from user
    @return N/A
    '''
    def set_msg(self,msg): 
        self.msg=msg
    '''
    This function switches the message into a list of letters using what was learned in intro to programming
    @param self,key for encrypting message,msg for getting message from user
    @return N/A
    '''
    def letter(self):
        self.word2char=[]
        for i in range(len(self.msg)):
            characters= [character for character in self.msg[i]]
            self.word2char.append(characters)   
    '''
    This method encrypts the message of the user by swapping letters in the message to an encrypted message using the key
    @param self
    @return encryption which is a string combined from a list of encrypted characters
    '''
    def encrypt(self):
        cipher=[]
        self.char2cip=[]
        for t in range (len(self.word2char)):
            ciphchar=[]
            for i in range(len(self.word2char[t])):
                if self.word2char[t][i]==" ":#if there is a space put it in the encryption
                    ciphchar.append(" ")
                for j in range(len(self.key)):
                    keys=list(self.key.keys())[j] #represents a key in dict
                    values=list(self.key.values())[j] #represents a value in dict
                    
                    if self.word2char[t][i]==keys: #checks if the the word is in the keys or values part of the dictionary key
                        ciphchar.append(values)
                    elif self.word2char[t][i]==values:
                        ciphchar.append(keys)
            self.char2ciph.append(ciphchar)            
        #convert character cipher into string cipher
        for l in range(len(self.char2ciph)): 
            combine=""
            for m in range (len(self.char2ciph[l])):
                combine+=self.char2ciph[l][m]
            cipher.append(combine)
        encryption= (''.join(cipher))
        return encryption
 

class CeaserEncryption(Encryption):
    '''
    This initializer method gets the key and message from the user
    @param self,key for encrypting message,msg for getting message from user
    @return N/A
    '''
    def __init__(self,key,msg=""):
        self.msg=msg
        self.key= key
        self.words2chars=[]#converts the words in list words to letters
        self.encrychars=[]#converts letters to encrypted letters 
    '''
    This function switches the message into a list of letters using what was learned in intro to programming
    @param self,key for encrypting message,msg for getting message from user
    @return N/A
    '''
    def letter(self):
        for i in range(len(self.msg)):
            characters= [character for character in self.msg[i]]
            self.words2chars.append(characters)    
    '''
    This mutator method allows the class to access the user input
    @param self,msg for getting message from user
    @return N/A
    '''
    def set_msg(self,msg): 
        self.msg=msg.lower()
    '''
    This method encrypts the message of the user by shifting each of the letters four to the right using the key
    @param self
    @return encryption which is a string combined from a list of encrypted characters
    '''
    def encrypt(self): #figure out how it will look as a fn
        cipher=[]
        for k in range(len(self.words2chars)):
            encrytemp=[]
            for m in range(len(self.words2chars[k])):
                if self.words2chars[k][m]==" ": #when there is a space make a space in the encrypted message
                    encrytemp.append(" ")
                for l in range(len(self.key)):
                    shift=(l+4)%26 #encryption using 4 to encrypt
                    if self.words2chars[k][m]==self.key[l]:
                        encrytemp.append(self.key[shift])
            self.encrychars.append(encrytemp)
            
        #encryption letters to encryption
        for n in range(len(self.encrychars)): 
            combine=""
            for o in range (len(self.encrychars[n])):
                combine+=self.encrychars[n][o]
            cipher.append(combine)
        encryption= (''.join(cipher))
        return encryption


class ProductEncryption(Encryption):
    '''
    This initializer method gets the key,and the message from the user
    @param self,key for encrypting message,msg for getting message from user
    @return N/A
    '''
    def __init__(self,key,msg=""):
        self.key= key
        self.trans_key = 3
        self.msg=msg
    '''
    This mutator method allows the class to access the user input
    @param self,msg for getting message from user
    @return N/A
    '''    
    def set_msg(self,msg):
        self.msg=msg
    '''
    This method encrypts the message by using the key to swap each of the letters or keeping it the same if not in key
    and is adjusted into columns according to the trans_key
    @param self
    @return encryption which is a string combined from a list of encrypted characters
    '''
    def encrypt(self):
        encryption=""
        sub_ciphertext = ""
        for char in self.msg:
            if char in self.key.keys():
                sub_ciphertext += self.key[char]
            else:
                sub_ciphertext += char
        ciphertext = [''] * self.trans_key
        for col in range(self.trans_key):
            position = col
            while position < len(sub_ciphertext):
                ciphertext[col] += sub_ciphertext[position]
                position += self.trans_key
        encryption=''.join(ciphertext) #Cipher text
        return encryption
    
       
class RSAEncryption(Encryption):
    '''
    This initializer method gets the key which is seperated into 3 parts p, q, and e where p and q are used to the modulus for private and public key.
    The e is used as an exponent for public key and the message from the user
    @param self,key using p,q,e for encrypting message, msg for getting message from user
    @return N/A
    '''
    def __init__(self, p, q, e,msg=""):
        self.msg = msg
        self.p = p
        self.q = q
        self.e = e
        self.n = p * q
        self.phi = ((p - 1) * (q - 1))
        self.d = self.multiplicative_inverse(e, self.phi)
        self.public = (self.e, self.n)
        self.private = (self.d, self.n)
    '''
    This mutator method allows the class to access the user input
    @param self,msg for getting message from user
    @return N/A
    ''' 
    def set_msg(self,msg):
        self.msg=msg   
    # makes use of the multiplicative inverse to calculate the decryption key
    '''
    This method calulates the decryption key
    @param self, e is the exponent for public key, and phi which is Eulers totient function
    @return d+phi
    '''
    def multiplicative_inverse(self, e, phi):
        d, x1, x2, y1, temp_phi = 0, 0, 1, 1, phi
        while e > 0:
            temp1 = temp_phi // e
            temp2 = temp_phi - temp1 * e
            temp_phi, e = e, temp2
            x = x2 - temp1 * x1
            y = d - temp1 * y1
            x2, x1, d, y1 = x1, x, y1, y
        if temp_phi == 1:
            return d + phi
    '''
    This encryption function encrypts the message and combines it to a string
    @param self
    @return encryption that takes the encryted message into a string
    '''
    def encrypt(self):
        combine=""
        encryption = [(ord(char) ** self.public[0]) % self.public[1] for char in self.msg]
        return encryption
    
    
'''
This inheritance class that is the parent for all the decryptions for the ciphers
'''
class Decryption(object):
    '''
    This initializer method holds values that are similar in all of the class initializers for encryption ciphers
    @param self,key holds the key used to encrypt,cip holds the encryption given by the user 
    @return N/A
    '''
    def __init__(self,key,cip=''):
        pass
    '''
    This mutator method is an overriding method for setting the encryption
    @param self,msg allows previously done encryption to be used in the class
    @return N/A
    '''
    def set_cip(self,cip):
        pass
    '''
    This decryption method is an overriding method for the decrypting the encryption
    @param self
    @return decryption this returns the encryption that was decrypted
    '''
    def decrypt(self):
        return Decryption
    
    
class TranspositionDecryption(Decryption):
    '''
    This initializer method gets the key,and the cipher from the encryption
    @param self,key for decrypting encryption,cip for getting encryption from previously encrypted text
    @return N/A
    ''' 
    def __init__(self, key,cip=''):
        self.key = key
        self.cip=cip
    '''
    This mutator method is an overriding method for setting the cipher
    @param self,cip allows the encryption to be used in the class
    @return N/A
    '''
    def set_cip(self,cip):
        self.cip=cip
    '''
    This decryption method is an overriding method for the decrypting the encryption using a number of columns based on the key
    @param self
    @return message this returns the encryption that was decrypted
    '''
    def decrypt(self):
        # Create the empty matrix
        row = len(self.cip) // len(self.key)
        decrypted_message = [[None] * len(self.key) for _ in range(row)]
        # Arrange the matrix in terms of the column according to key
        message_index = 0
        for k in sorted(self.key):
            index = self.key.index(k)
            for j in range(row):
                decrypted_message[j][index] = self.cip[message_index]
                message_index += 1
        # turn the matrix into a string
        message = "".join("".join(row) for row in decrypted_message)
        # Remove added characters
        message = message.replace("*", "")
        return message
    
class PlayfairDecryption:
    '''
    This initializer method holds key which is the method of encrypting, and the encryption that was done
    @param self,key holds the key used to decrypt,cip holds the encryption
    @return N/A
    '''
    def __init__(self, key,cip=""):
        self.key = key
        self.cip=cip
        self.key_matrix = self.generate_key_matrix()  # generate the key matrix using the provided key
    '''
    This mutator method is an overriding method for setting the encryption
    @param self,cip allows encryption to be used in the class
    @return N/A
    '''
    def set_cip(self,cip):
        self.cip=cip
    '''
    This method makes the 5x5 matrix that will be used for the rules in the further methods
    @param self
    @return key_matrix this is the 5x5 matrix
    '''
    def generate_key_matrix(self):
        a_to_z = string.ascii_lowercase.replace('j', ' ') # create a string of all the lowercase letters except for 'j'
        key_matrix = ['' ] * 5 # initialize the key matrix as a list of 5 empty strings
      # variables to keep track of the current row and column in the key matrix
        key_count= 0
        row_count = 0
      # iterate through the characters in the provided key
        for characters in self.key:
            if characters in a_to_z and characters != ' ': # if the character is a valid lowercase letter (excluding 'j')
                key_matrix[key_count] += characters # add the character to the current row in the key matrix
                a_to_z = a_to_z.replace(characters, ' ') # remove the character from the list of available characters
                row_count += 1 #increment the row count
              #if the current row is full, move onto the next row
                if row_count == 5:
                    key_count += 1
                    row_count = 0 # reset the row count
        for characters in a_to_z: # fill in the remaining spaces in the key matrix with the remaining letters from a_to_z
            if characters != ' ':
                if key_count < 5 and row_count < 5:
                    key_matrix[key_count] += characters
                    row_count += 1
                    if row_count == 5:
                        key_count += 1
                        row_count = 0
        return key_matrix
    '''
    This decryption method adds an x if 2 letters next to eachother are same or adds them together if they arent into plaintextpairs
    then checks if the letters in each of the plainpairs are in the same row and swaps each to the character left of it if its true 
    or if its in the same column each letter in plaintextpair swaps with a chacter above it and if both arent the case then creates a
    rectangle with each letter in plaintextpair in opposite corners of the rectangle in key_matrix and swaps characters in the row of 
    each letter in plaintextpair and if there is an x present replace it with the letter left of it
    @param self
    @return message2 the final encrypted text
    '''
    def decrypt(self):
        plaintextpairs = []
        ciphertextpairs = []
        i = 0
        while i < (len(self.cip)):
            first_letter = self.cip[i]
            second_letter = self.cip[i + 1]
          # If the two letters in the ciphertext pair are the same,
          # replace the second letter with 'x' and reduce the index i by 1
          # so that we don't skip the next letter in the ciphertext string
            if first_letter == second_letter:
                second_letter = 'x'
                i -= 1
              # Add the ciphertext pair to the list of ciphertext pairs
            ciphertextpairs.append(first_letter + second_letter)
            i = i + 2
      # Loop through each ciphertext pair and reverse the encryption rules
        for pair in ciphertextpairs:
            applied_rule = False
          # Check each row in the key matrix to see if the pair is present
          # and apply the decryption rule if it is
            for row in self.key_matrix:
                if pair[0] in row and pair[1] in row:
                    j0 = row.find(pair[0])
                    j1 = row.find(pair[1])
                    plaintextpair = row[(j0 - 1) % 5] + row[(j1 - 1) % 5]
                    plaintextpairs.append(plaintextpair)
                    applied_rule = True
          # If the rule has been applied, move on to the next ciphertext pair
            if applied_rule:
                continue
          # Check each column in the key matrix to see if the pair is present
          # and apply the decryption rule if it is
            for j in range(5):
                col = "".join([self.key_matrix[i][j] for i in range(5)])
                if pair[0] in col and pair[1] in col:
                    i0 = col.find(pair[0])
                    i1 = col.find(pair[1])
                    plaintextpair = col[(i0 - 1) % 5] + col[(i1 - 1) % 5]
                    plaintextpairs.append(plaintextpair)
                    applied_rule = True
          # If the rule has been applied, move on to the next ciphertext pair
            if applied_rule:
                continue
          # If the pair is not in the same row or column, it must be in
          # a diagonal, so apply the final decryption rule
            i0, i1, j0, j1 = 0, 0 , 0, 0
            for i in range(5):
                row = self.key_matrix[i]
                if pair[0] in row:
                    i0 = i
                    j0 = row.find(pair[0])

                if pair[1] in row:
                    i1 = i
                    j1 = row.find(pair[1])
            plaintextpair = self.key_matrix[i0][j1] + self.key_matrix[i1][j0]
            plaintextpairs.append(plaintextpair)
        for i in range(len(plaintextpairs)):
            for j in range(len(plaintextpairs[i])):
                if plaintextpairs[i][j]=="z":
                    plaintextpairs[i][j]=" "
      # Combine the plaintext pairs into a single string
        plaintext = "".join(plaintextpairs)
      # If the last letter in the plaintext is an 'x', remove it
        if plaintext[-1] == 'x':
            plaintext = plaintext[:-1]
#if there is an x in the decrypted message, replace it with the letter to the left of it
        message1 = list(plaintext)
        if 'x' in message1:
            idx =                 message1.index('x')
            if idx > 0:
                message1[idx] = message1[idx - 1]
            else:
                message1[idx] = ''
        message2= (''.join(message1))
        return message2


class SubsitutionDecryption(Decryption):
    '''
    This initializer method gets the set key and cipher from the encryption 
    @param self,key for decrypting message,cip for getting cipher from the encryption
    @return N/A
    '''
    def __init__(self,key,cip=""):
        self.cip= cip#put words into a list
        self.key = key #have alpha conversion as dict
        self.char2ciph=[] #convert list of characters to ciphered list of characters
        self.ciph2char=[] #convert list of cipher characters to characters    
    '''
    This function switches the message into a list of letters using what was learned in intro to programming
    @param self,key for encrypting message,msg for getting message from user
    @return N/A
    '''
    def letter(self):
        for i in range(len(self.cip)):
            characters= [character for character in self.cip[i]]
            self.char2ciph.append(characters)
        return self.char2ciph
    '''
    This mutator method allows the class to access encryption that was done
    @param self,cip from the encryption
    @return N/A
    '''
    def set_cip(self,cip): 
        self.cip=cip
    '''
    This method decrypts the encryption by swapping letters in the encryption to a message using the key
    @param self
    @return decryption which is a string combined from a list of decrypted characters
    '''
    def decrypt(self):
        word=[]
        for n in range(len(self.char2ciph)):
            wordchar=[]
            for o in range(len(self.char2ciph[n])):
                if self.char2ciph[n][o]==" ":
                    wordchar.append(" ")
                for p in range(len(self.key)):
                    key=list(self.key.keys())[p]#represents keys in dict
                    value=list(self.key.values())[p]#represents values in dict
                    if self.char2ciph[n][o]==key: #check if character from encryption matches dict key
                        wordchar.append(value)
                    elif self.char2ciph[n][o]==value:#check if character from encryption matches dict value
                        wordchar.append(key)
            self.ciph2char.append(wordchar)
        for q in range(len(self.ciph2char)):
            combine=""
            for r in range(len(self.ciph2char[q])):
                combine+=self.ciph2char[q][r]
            word.append(combine)
        decryption = (''.join(word))
        return decryption
    
    
class CeaserDecryption(Decryption):
    '''
    This initializer method gets the set key and cipher from the encryption 
    @param self,key for decrypting message,cip for getting cipher from the encryption
    @return N/A
    '''
    def __init__(self,key,cip=""):
        self.cip= cip
        self.key= key
        self.encrychars=[]#converts letters to encrypted letters
        self.wordchars=[]#converts encrypted letters to letteres
    '''
    This mutator method allows the class to access encryption that was done
    @param self,cip from the encryption
    @return N/A
    '''    
    def set_cip(self,cip): 
        self.cip=cip.lower()
    '''
    This function switches the message into a list of letters using what was learned in intro to programming
    @param self,key for encrypting message,msg for getting message from user
    @return N/A
    '''
    def letter(self):
        for i in range(len(self.cip)):
            characters= [character for character in self.cip[i]]
            self.encrychars.append(characters)
    '''
    This method decrypts the encryption by reversing the shift to letters four to the left using the key
    @param self
    @return decryption which is a string combined from a list of decrypted characters
    '''
    def decrypt(self):
        word=[]
        for p in range(len(self.encrychars)):
            wordtemp=[]
            for q in range(len(self.encrychars[p])):
                if self.encrychars[p][q]==" ": #when there is a space make a space in the encrypted message
                    wordtemp.append(" ")
                for r in range(len(self.key)):
                    rshift=(r-4)%26
                    if self.encrychars[p][q]==self.key[r]:
                        wordtemp.append(self.key[rshift])
            self.wordchars.append(wordtemp)
        for s in range(len(self.wordchars)):
            combine=""
            for t in range(len(self.wordchars[s])):
                combine+=self.wordchars[s][t]
            word.append(combine)
        decry = (''.join(word))
        return decry

    
class ProductDecryption(Decryption):  
    '''
    This initializer method gets the set key and cipher from the encryption 
    @param self,key for decrypting message,cip for getting cipher from the encryption
    @return N/A
    '''
    def __init__(self,key,cip=""):
        self.key= key
        self.trans_key = 3
        self.cip=cip
    '''
    This mutator method allows the class to access encryption that was done
    @param self,cip from the encryption
    @return N/A
    '''    
    def set_cip(self,cip):
        self.cip=cip
    '''
    This method decrypts by using number of lines and columns based on the length of encryption and transkey 
    and decrypts by reading the rows and columns
    @param self
    @return plaintect which is a string combined from a list of decrypted characters
    '''
    def decrypt(self):
        numOfColumns = math.ceil(len(self.cip) / self.trans_key)
        numOfRows = self.trans_key
        numOfShadedBoxes = (numOfColumns * numOfRows) - len(self.cip)
        plaintext = [''] * numOfColumns
        col = 0
        row = 0
        for symbol in self.cip:
            plaintext[col] += symbol
            col += 1
            if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
                col = 0 
                row += 1 
        sub_ciphertext = ''.join(plaintext)
        plaintext = ""
        for char in sub_ciphertext:
            if char in self.key.values():
                plaintext += list(sub_key.keys())[list(sub_key.values()).index(char)]
            else:
                plaintext += char
        return plaintext

    
class RSADecryption(Decryption):
    '''
    This initializer method gets the key which is seperated into 3 parts p, q, and e where p and q are used to the modulus for private and public key.
    The e is used as an exponent for public key and the cip from the encryption
    @param self,key using p,q,e for decrypting message, cip for getting encryption
    @return N/A
    '''
    def __init__(self, p, q, e,cip=""):
        self.cip= cip
        self.p = p
        self.q = q
        self.e = e
        self.n = p * q
        self.phi = ((p - 1) * (q - 1))
        self.d = self.multiplicative_inverse(e, self.phi)
        self.public = (self.e, self.n)
        self.private = (self.d, self.n)
    '''
    This mutator method allows the class to access encryption that was done
    @param self,cip from the encryption
    @return N/A
    '''    
    def set_cip(self,cip):
        self.cip=cip
    '''
    This method calulates the private key d using the multiplicative inverse
    @param self, e is the exponent for public key, and phi which is Eulers totient function
    @return d+phi
    '''
    def multiplicative_inverse(self, e, phi):
        d, x1, x2, y1, temp_phi = 0, 0, 1, 1, phi
        while e > 0:
            temp1 = temp_phi // e
            temp2 = temp_phi - temp1 * e
            temp_phi, e = e, temp2
            x = x2 - temp1 * x1
            y = d - temp1 * y1
            x2, x1, d, y1 = x1, x, y1, y
        if temp_phi == 1:
            return d + phi
    '''
    This decryption function decrypts the message and combines it to a string
    @param self
    @return decryption that takes the decryted message into a string
    '''
    def decrypt(self):
        decryption=""
        plain = [chr((char ** self.private[0]) % self.private[1]) for char in self.cip]
        decryption=''.join(plain)
        return decryption


obj = Message()
halt=False #check if user says STOP
words=[]#holds all the words that user input
numlist=[]#numbers that will correspond to a cipher to pick a cipher for encrypting the message
while halt != True:#adds words from user until user types STOP 
    try:
        userInp=input("Enter message:")
        assert userInp.isalpha() #check if the user only typed letters
    except AssertionError:#this error handler checks if the user doesn't use numbers and special characters
        print("Error: A word expected received an integer or spaces or punctuations")
    else:
        print("...Encrypting Message...")
        if userInp!="STOP":
            words.append(userInp)
        else:
            halt = True
for i in range(len(words)):#takes the words and adds it to the message class 
    obj.set_words(words[i])
for i in range(len(words)):#take the length of words from the user and appends random number from 1-6 to numlist
    numlist.append(obj.assignCipher())

for i in range(len(numlist)):#checks which number is in numlist and picks an cipher to encrypt and decrypt and prints it to the user
    print()
    if numlist[i]==1:
        transEn = TranspositionEncryption("pen")
        transEn.set_msg(words[i])
        transDe = TranspositionDecryption("pen")
        transDe.set_cip(transEn.encrypt())
        print("Plaintext Message:" +transDe.decrypt())
        print("Encrypted Message:" +transEn.encrypt())
        print("Method: Transposition")
    if numlist[i]==2:
        playEn = PlayfairEncryption("secretkey")
        playEn.set_msg(words[i])
        playDe = PlayfairDecryption("secretkey")
        playDe.set_cip(playEn.encrypt())
        print("Plaintext Message:" +playDe.decrypt())
        print("Encrypted Message:" +playEn.encrypt())
        print("Method: PlayFair")
    if numlist[i]==3:
        subEn = SubsitutionEncryption({"a":"z","b":"y","c":"x","d":"w","e":"v","f":"u","g":"t","h":"s","i":"r","j":"q","k":"p","l":"o","m":"n","A":"Z","B":"Y","C":"X","D":"W","E":"V","F":"U","G":"T","H":"S","I":"R","J":"Q","K":"P","L":"O","M":"N"})
        subEn.set_msg(words[i])
        subEn.letter()
        subDe = SubsitutionDecryption({'a': 'z', 'b': 'y', 'c': 'x', 'd': 'w', 'e': 'v', 'f': 'u', 'g': 't', 'h': 's', 'i': 'r', 'j': 'q', 'k': 'p', 'l': 'o', 'm': 'n', 'A': 'Z', 'B': 'Y', 'C': 'X', 'D': 'W', 'E': 'V', 'F': 'U', 'G': 'T', 'H': 'S', 'I': 'R', 'J': 'Q', 'K': 'P', 'L': 'O', 'M': 'N'})
        encry=subEn.encrypt()
        subDe.set_cip(encry)
        subDe.letter()
        print("Plaintext Message:" +subDe.decrypt())
        print("Encrypted Message:" +encry)
        print("Method: Subsitution")
    if numlist[i]==4:
        ceaEn = CeaserEncryption({0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h",8:"i",9:"j",10:"k",11:"l",12:"m",13:"n",14:"o",15:"p",16:"q",17:"r",18:"s",19:"t",20:"u",21:"v",22:"w",23:"x",24:"y",25:"z"})
        ceaEn.set_msg(words[i])
        ceaEn.letter()
        ceaDe = CeaserDecryption({0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h",8:"i",9:"j",10:"k",11:"l",12:"m",13:"n",14:"o",15:"p",16:"q",17:"r",18:"s",19:"t",20:"u",21:"v",22:"w",23:"x",24:"y",25:"z"})
        encry=ceaEn.encrypt()
        ceaDe.set_cip(encry)
        ceaDe.letter()
        print("Plaintext Message:" +ceaDe.decrypt())
        print("Encrypted Message:" +encry)
        print("Method: Ceaser")
    if numlist[i]==5:
        proEn = ProductEncryption({"A": "Z", "B": "Y", "C": "X", "D": "W", "E": "V", "F": "U", "G": "T", "H": "S", "I": "R", "J": "Q", "K": "P", "L": "O", "M": "N", "N": "M", "O": "L", "P": "K", "Q": "J", "R": "I", "S": "H", "T": "G", "U": "F", "V": "E", "W": "D", "X": "C", "Y": "B", "Z": "A"})
        proEn.set_msg(words[i])
        proDe = ProductDecryption( {"A": "Z", "B": "Y", "C": "X", "D": "W", "E": "V", "F": "U", "G": "T", "H": "S", "I": "R", "J": "Q", "K": "P", "L": "O", "M": "N", "N": "M", "O": "L", "P": "K", "Q": "J", "R": "I", "S": "H", "T": "G", "U": "F", "V": "E", "W": "D", "X": "C", "Y": "B", "Z": "A"})
        proDe.set_cip(proEn.encrypt())
        print("Plaintext Message:" +proDe.decrypt())
        print("Encrypted Message:" +proEn.encrypt())
        print("Method: Product")
    if numlist[i]==6:
        rsaEn = RSAEncryption(17,13,7)
        rsaEn.set_msg(words[i])
        rsaDe = RSADecryption(17,13,7)
        rsaDe.set_cip(rsaEn.encrypt())
        print(f"Plaintext Message: {rsaDe.decrypt()}")
        print(f"Encrypted Message: {rsaEn.encrypt()}")
        print("Method: RSA")

