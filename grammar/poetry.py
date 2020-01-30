from random import choice

terminals = []
non_terminals = []
punctuation = ['Period','Comma','Semicolon']
D = {'Period':'.', 'Comma':',', 'Semicolon':';'}

def readTerminal(f):
    global terminals
    name = f.readline().rstrip()
    if name=='':
        return False
    D[name] = []
    terminals += [name]
    while True:
        line = f.readline().rstrip().lower()
        if line=='': break
        D[name] += [line]
    return True

def readNonTerminal(f):
    global non_terminals
    name = f.readline().rstrip()
    if name=='':
        return False
    D[name] = []
    non_terminals += [name]
    while True:
        line = f.readline().rstrip()
        if line=='': break
        D[name] += [line.split(' ')]
    return True

def readFiles(term, non_term):
    with open(term) as f:
        remaining = True
        while remaining:
            remaining = readTerminal(f)
    with open(non_term) as f:
        remaining = True
        while remaining:
            remaining = readNonTerminal(f)

def generate(item):
    s = ''
    if item in non_terminals:
        for part in choice(D[item]):
            s += generate(part)
    elif item in terminals:
        s = ' ' + choice(D[item])
    elif item in punctuation:
        s = D[item]
    return s

if __name__=='__main__':
    readFiles('terminals.txt', 'non_terminals.txt') 
    for l in range(3):
        sentence = generate('S')[1:].capitalize() + '.'
        print(sentence)
    
