alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def invertkey(key):
    new = ''
    for letter in alphabet:
        new += alphabet[key.index(letter)]
    return new
