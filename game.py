import random


class Mastermind:
    def __init__(self, colors):
        self.colors = colors
        self.combination = None
        self.repetitions = True
        
    def new_game(self, repetitions=False):
        self.repetitions = repetitions
        if repetitions:
            self.combination = [random.choice(self.colors) for _ in range(4)]
        else:
            c = list(self.colors)
            random.shuffle(c)
            self.combination = c[:4]
            del c


    def evaluate(self, c):
        perfects = 0    # Bonne couleur bien placée
        goods = 0       # Bonne couleur mal placée
        combi = list(self.combination)
        cbis = list(c)
        for i in range(4):
            if c[i] == self.combination[i]:
                perfects += 1
        combi = [self.combination[i] for i in range(4) if self.combination[i] != c[i]]
        cbis = [c[i] for i in range(4) if self.combination[i] != c[i]]
                
        for i in range(len(cbis)):
            if cbis[i] in combi:
                goods += 1
                #cbis.remove(c[i])
            
        return perfects, goods
            
        

if __name__ == '__main__':
    COLORS = [1,2,3,4,5,6,7,8]

    game = Mastermind(COLORS)
    game.new_game(repetitions=False)
    
    game.combination = (1,2,3,2)
    print(game.evaluate((9,2,9,9)))
    print(game.evaluate((2,9,9,9)))
    
    while True:
        c = input('\n> ')
        c = [int(i) for i in list(c)]
        print(game.evaluate(c))