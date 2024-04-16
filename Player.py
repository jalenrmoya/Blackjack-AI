import random as rand
from Game import Game

# BlackJack Player Class

# Dealer Class uses a basic strategy of hitting until the value 
# of the hand is 17 or greater
class Dealer: 
    def __init__(self):
        # self.hand = []
        self.value = 0
        self.game = Game()
    
    def get_move(self, game, hand):
        self.value = game.calculateScore(hand)
        if self.value < 17:
            return "hit"
        else:
            return "stand"
        
# ManualPlayer Class allows the user to input their move
class ManualPlayer:
    def __init__(self):
        self.hand = []
        self.value = 0
        self.game = Game()
    
    def get_move(self, game, hand):
        self.value = game.calculateScore(hand)
        self.hand = hand
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

    def get_move(self, game, hand):
        self.value = game.calculateScore(hand)
        self.hand = hand
        if rand.random() < 0.5:
            return "hit"
        else:
            return "stand"


class CardCountingPlayer:
    def __init__(self, num_decks):
        self.hand = []
        self.value = 0
        self.count = 0
        self.num_decks = num_decks

    def get_move(self, game, hand):
        self.hand = hand
        self.value = game.calculateScore(hand)
        self.update_count(hand)

        # Basic strategy based on count
        if self.count >= 2:
            # Bet more when count is high
            if self.value < 17 and game.board[0][1] < 7:
                return "hit"
            else:
                return "stand"
        else:
            # Bet less when count is low
            if self.value < 17:
                return "hit"
            else:
                return "stand"

    def update_count(self, hand):
        """Update the running card count based on the cards in the hand."""
        for card in hand:
            if card in [2, 3, 4, 5, 6]:
                self.count += 1
            elif card in [10, "J", "Q", "K", "A"]:
                self.count -= 1
        self.count = min(max(-self.num_decks * 10, self.count), self.num_decks * 10)
        
        
     
# Kind of a Nearest Neighbor algorithm I think? 
# it compares the players hand to the dealer and a 21 value 
# and "classifies" the hand as hit or stand
class NearestNeighborPlayer:
    def __init__(self):
        pass

    def get_move(self, game, player_hand):
        player_value = game.calculateScore(player_hand)
        dealer_value = game.calculateScore(game.players[0])  # Assume only the dealer's visible card matters

        # Calculate the difference between the player's hand value and the dealer's hand value
        player_diff = abs(dealer_value - 21)

        # Calculate the difference between the player's hand value and 21
        player_diff_to_21 = abs(player_value - 21)

        # If hitting would not cause the player to bust and getting closer to 21 than the dealer, hit
        if player_value < 21 and player_diff_to_21 > player_diff:
            return "hit"

        # Otherwise, stand
        return "stand"

