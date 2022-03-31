import collections
import numpy as np

def main():
    # Hardcoding cipher text
    cipher_text = "LAVHEBSJMDINFGXCLWTUUWARWBQWFTEHWUDDTCAAKKTXTSMYALMVHTAHJHKICFAFZKLEXATXIXYMFVLVGUDALRFJTTGKXNLOYOWLVVVQAFKVGEZLEHEXHEZGPVZEDOWARZEAFSGVASOSDXJIEZESBEWTDWSFGVOPMUMJENPKWKMMCQKVXJMGZWVBEEWMQLARXGUNWLLWEDKKHCICAFLKFPOHWJTTGEEKLHKLEUJVTKEAESJXJYLFDSPVRFAJUXDINFAKLFQEFAEXJYNMTDXKSRQUGOVVTTWUHEXEZLGYVPEOLJHEMCOGEFLRIOSLBFRSRJGFKLEFWUAESLAYQIISVUVWKVZEZAFKVWPAFKXKSAOGMKKSRPWJHIHUXQSNKLODARXUAADJSGKMSEMWWSCARWVXIELVMVZVJODWPTDTLQESGPGOYEMGZGAFAGGJWEDNAVVWNAOWGTVYBLUXIXAUFUHDQUZAUTKMOZKTRUIFMMDMNMTTLZXBIYZWUXJWADQLHUICDQHMKLEOGEFLRIOSLBFRSEGDXCCIZLZXYENPKGYKLEQFVNJIRFZALRTPXAWLSSTTOZXEXHQVSMRMSUFEHKMOZGNXIILQULKFRIOFWMNSRWKGKRXRQKLHEENQDWVKVOZAUWVZIOWAYKLEOGEFLRIOSLBFRSBJGOZHEDAKLVVVQVOBKLAISJKRRTEWWDZRGFZGLVGOYEMGZGAFAGGJXHQHJHMMDQJUTEROFHJHMMDQLZXUETMTWVRYSQALARWDQKAZEIDFZWMVGHZGDHXCSGUZMYETULUTEROFTWTTGEEKWWSCAZQLAZVDBSJMPAEPGFHKLAHWSGPWIXNWKSYLXWLLRRDFZWWZWCGKKBFRSIALAZRTTWWQVGUFANXSVAZUZTIISFADEFRGAAFZNLIXWLAVVETSKGFXYQLTXVRAPWUBJMOZOZXKLEDLGLVIKXWYBJPAFAGGNIMGKLPFVKIALATSNSJWLJMNPMKMICAOSVXDMCEHJBMECKYJHLTSMFVHKLEDKLHTVARLSGRTPDGSVYXHMLSWUVEEKWLRPLAXLAVQUXLAICICAEHXKMNSUGGTIRZKLARXHMNWUVINFZWYFGUEGXLFQUOZVXSETQTMMNICMFSECEGDWWMYETIWOBCPNQWVHEKOUFYAFREELSGUMNRGJFVHPGTDBTHENSLXRFOGLZHNFEELLHGVOFWUMCMBQJLRRRDEWUNIMTKAFUFXHAMJERASMFVHLVTQUZGFPOSQ"
    cipher_text = cipher_text.upper() #ensuring everything's upper
    # PART 1:__________________________________________
   
    # Loop over all values of m, compute and print out index of coincidences for substrings
    # and the average
    max_coincidence = -1
    max_m = 4
    for m in [4,5,6,7,8]:
        substrings = split_substrings(m, cipher_text)
        substring_number = 0
        total = 0
        for substring in substrings:
            substring_number = substring_number + 1
            index = index_of_coincidence(substring)
            total = total + index
            print("[m=%d] Index of coincidence for substring %d is: %f" % (m, substring_number, index))
        print("Average index of coincidence for m = %d: %f\n" % (m, total/m))

    # PART 2: Finds the key with the substrings with length 7
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    m = 7
    substrings = split_substrings(m, "lbfb")
    table = [[0 for col in range(m)] for row in range(26)]
    ideal_letter_frequency = [.082, .015, .028, .043, .127, .022, .02, .061, .07, .002, .008, .04, .024, .067, .075, .019, .001, .06, .063, .091, .028, .01, .023, .001, .02, .001]
    substring_number = 0
    
    #Calculates the product from the frequencies of the English language and the ciphertext
    #Then gives the highest dot product for each of the substrings to find the key
    highest_dot_products = [[0 for row in range(2)] for column in range(m)] #letter position, dot product
    for substring in substrings:
        # Give frequency of letters as percentage of total letters
        letter_frequency = get_letter_frequencey(substring)
        frequency_percentage = []
        for letter in alphabet:
            frequency_percentage.append(letter_frequency[letter]/len(substring)*100)
        for i in range(26):
            # takes the dot product of the frequency and ideal frequency 
            dot_product = np.dot(frequency_percentage, ideal_letter_frequency)
            table[i][substring_number] = dot_product
            frequency_percentage = np.roll(frequency_percentage, 1)
            #singling out the highest dot product
            if dot_product > highest_dot_products[substring_number][1]:
                highest_dot_products[substring_number] = [i, dot_product]
        substring_number = substring_number + 1   
    print(["       M1       ,           M2      ,         M3       ,         M4        ,         M5       ,          M6       ,         M7     "])        
    for row in range(len(table)):
        print(table[row]) 
    print('\n')
    for row in range(len(highest_dot_products)):
        print(highest_dot_products[row])
    print('\n')
    
    #prints the key    
    print("The key is: " + alphabet[8], alphabet[7], alphabet[9],alphabet[22],alphabet[0],alphabet[14],alphabet[8])
    
    
    # PART 3____________________________________________________
    key = "IHJWAOI"
    m = 7
    key = [8, 7, 9, 22, 0, 14, 8]
    plain_text = ""
    
    #Decodes the ciphertext into an unformatted plaintext
    for i in range(len(cipher_text)):
        plain_letter = to_letter((to_number(cipher_text[i]) + key[i % m]) % 26)
        plain_text = plain_text + plain_letter
    print("The Unformatted Plaintext is: \n" + plain_text)
    
    
# This function returns the computed index of coincidence
# for a given ciphertext
def index_of_coincidence(cipher_text):
    # Get frequency of letters in dictionary in English
    frequency_table = get_letter_frequencey(cipher_text)
    number_of_letters = len(cipher_text)

    denominator = number_of_letters * (number_of_letters - 1)
    numerator = 0
    for letter in frequency_table.keys():
        frequency = frequency_table[letter]
        numerator = numerator + (frequency * (frequency - 1))
    return numerator/denominator


#This function splits the strings into substrings with a given length m
def split_substrings(m, cipher_text):
    substrings = []
    for i in range(m):
        substrings.append("")
    for i in range(len(cipher_text)):
        substrings[(i % m)] = substrings[(i % m)] + cipher_text[i]
    return substrings


# This function returns a dictionary containing the frequency of each letter contained inside of a body of text
def get_letter_frequencey(text):
    return {char : text.count(char) for char in set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}


#This calculates the dot product of the two vectors
def dot_product(vector1, vector2):
    total = 0
    for i in range(len(vector1)):
        total = total + vector1[i] * vector2[i]
    return total


#Converts the numbers to the letters
def to_letter(number):
    number = number % 26
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return alphabet[number]


#Converts the letters to the numbers
def to_number(letter):
    letter = letter.lower()
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return alphabet.index(letter)

if __name__ == "__main__":
    main() 