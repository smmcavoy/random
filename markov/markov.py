from random import choice
FILE = 'bible.txt'
ORDER = 10 

def remove(s, char):
    s2 = ''
    for i in range(len(s)):
        if s[i]==char:
            continue
        s2 += s[i]
    return s2

class NGram:
    def __init__(self, order=ORDER):
        self.occurences = {}
        self.total = 0
        self.order = order

    def __repr__(self):
        return 'NGram(' + str(self.total) +')'

    def addInstance(self, letter):
        try:
            self.occurences[letter] += 1
        except KeyError:
            self.occurences[letter] = 1
        self.total += 1

    def generateChar(self):
        s = ''
        for i in self.occurences:
            s += i * self.occurences[i]
        return choice(s)

class textGenerator:
    def __init__(self, order = ORDER):
        self.data = {}
        self.order = order
        self.starting_states = []

    def readLine(self, l):
        l = remove(l, '\n')
        if len(l)>= self.order:
            self.starting_states += [l[:self.order]]
        for i in range(self.order, len(l)):
            gram = l[i-self.order:i]
            try:
                self.data[gram].addInstance(l[i])
            except KeyError:
                self.data[gram] = NGram()
                self.data[gram].addInstance(l[i])

    def generateText(self, endChar = '.'):
        s = choice(self.starting_states)
        while s[-1] != endChar: 
            gram = s[-self.order:]
            try:
                s += self.data[gram].generateChar()
            except KeyError:
                break
        return s

if __name__=='__main__':
    t = textGenerator()
    with open(FILE) as f:
        while True:
            line = f.readline()
            if line.find('***EOF***') != -1: break
            t.readLine(line)
    while True:
        i = str(input('generate? (y/n) : '))
        if i.lower()=='n':
            break
        else:
            print(t.generateText())
        
                




