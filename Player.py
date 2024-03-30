import random as rand
from Game import Game

# BlackJack Player Class

# Dealer Class uses a basic strategy of hitting until the value 
# of the hand is 17 or greater
class Dealer: 
    def __init__(self):
        self.hand = []
        self.value = 0
        self.bust = False
        self.blackjack = False
        self.game = Game()
    
    def get_move(self, game):
        if self.value < 17:
            return "hit"
        else:
            return "stand"
        
# ManualPlayer Class allows the user to input their move
class ManualPlayer:
    def __init__(self):
        self.hand = []
        self.value = 0
        self.bust = False
        self.blackjack = False
        self.game = Game()
    
    def get_move(self, game):
        while True:
            move = input("Enter 'h' to hit or 's' to stand: ").lower()
            if move == 'h':
                return "hit"
            elif move == 's':
                return "stand"
            else:
                print("Invalid move. Please try again.")
    
# RandomPlayer Class randomly selects a move
# 50/50
class RandomPlayer:
    def __init__(self):
        self.hand = []
        self.value = 0
        self.bust = False
        self.blackjack = False

    def get_move(self, game):
        if rand.random() < 0.5:
            return "hit"
        else:
            return "stand"
        