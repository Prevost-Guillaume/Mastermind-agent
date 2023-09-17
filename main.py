from game import Mastermind
import itertools
from tqdm import tqdm
import numpy as np
import random


class Agent:
    def __init__(self, mastermind=Mastermind, verbose=True):
        self.colors = mastermind.colors
        self.mastermind = mastermind
        self.staying_combis = list(itertools.product(self.colors, repeat=4))
        if not mastermind.repetitions:
            self.staying_combis = [c for c in self.staying_combis if len(set(c))==4]
        self.possible_returns = [(0,0),(0,1),(0,2),(0,3),(0,4),
                                 (1,0),(1,1),(1,2),(1,3),
                                 (2,0),(2,1),(2,2),
                                 (3,0), (4,0)]  # (3,1) not possible
        self.turn = 0
        self.verbose = verbose
    
    
    def play(self):
        self.turn += 1
        if self.turn == 1:
            c = [1,2,3,4]
        elif self.turn == 2:
            c = [5,6,7,8]
        else:
            c = self.getBestMove()
        r = self.mastermind.evaluate(c)
        new_self_sc = [sc for sc in self.staying_combis if self.is_compatible(sc, c, r)]
        self.staying_combis = list(new_self_sc)
        if self.verbose:
            print(f'{r[0]}  |  {c[0]} {c[1]} {c[2]} {c[3]}  |  {r[1]}       => search space : {len(self.staying_combis)}')
        return c
        
        
    def getBestMove(self):
        return self.staying_combis[0]
        # Following code is useless : score for each staying combi is identical
        best_score, best_combi = len(self.staying_combis), None
        for combi in tqdm(self.staying_combis):
            score = self.get_score(combi)
            if score < best_score:
                best_score = score
                best_combi = combi
        return best_combi
        
        
    def get_score(self, combi):
        s = 0
        for r in self.possible_returns[:-1]:
            for sc in self.staying_combis:
                if self.is_compatible(sc, combi, r):
                    s += 1
        return s
        
    
    def is_compatible(self, sc, c, r):
        '''
        teste si la combi sc peut etre compatible avec le return r sur la combi c :
        1234 1243 (2,2) => True
        5678 1234 (2,2) => False
        5678 1234 (0,0) => True
        '''
        g = Mastermind(colors=self.colors)
        g.combination = sc
        p,g = g.evaluate(c)
        return p==r[0] and g==r[1]

        
                
    

if __name__ == '__main__':
    #AVG NB OF PLAYS : 4.95
    # MAX NB OF PLAYS : 10
     
    COLORS = [1,2,3,4,5,6,7,8]

    game = Mastermind(COLORS)
    game.new_game(repetitions=False)
    c = game.combination

    agent = Agent(game, verbose=True)

    print('\nRandomly chosen combinantion : ',game.combination)
    print('On left : nb of correct pawns')
    print('On right : nb of misplaced pawns of the correct color')
    print(f'\nX  |  {c[0]} {c[1]} {c[2]} {c[3]}  |  X       => search space : {len(agent.staying_combis)}')
    print(f'-------------------')

        
    move = agent.play()
    while list(move) != list(game.combination):# and len(agent.staying_combis)>1:
        move = agent.play()
    print('\nCONBINATION : ',move,'\n')
    
    
    
    ## Counter for mean and max number of moves
    if False:
        lm = []
        game = Mastermind(COLORS)
        game.new_game(repetitions=True)
        a = Agent(game)
        for c in tqdm(a.staying_combis):
            game = Mastermind(COLORS)
            game.new_game(repetitions=True)
            game.combination = c    
            agent = Agent(game, verbose=False)
            m = 1
            move = agent.play()
            while list(move) != list(game.combination):# and len(agent.staying_combis)>1:
                move = agent.play()
                m += 1
            lm.append(m)
        
        print(max(lm))
        print(sum(lm)/len(lm))
