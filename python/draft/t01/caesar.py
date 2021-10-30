# A python program to illustrate Caesar Cipher Technique
# https://www.geeksforgeeks.org/caesar-cipher-in-cryptography/


def encrypt(text, s):
    result = ""

    # traverse text
    for i in range(len(text)):
        char = text[i]

        # Encrypt uppercase characters
        if char.isupper():
            result += chr((ord(char) + s - 65) % 26 + 65)

        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)

    return result


# check the above function
s_encrypt = 4
text_encrypt = "AhojTomano"
# text_decrypt = "ElsnXsqers"
# s = 26 - s_encrypt
print("Text  : " + text_encrypt)
print("Shift : " + str(s_encrypt))
print("Cipher: " + encrypt(text_encrypt, s_encrypt))
