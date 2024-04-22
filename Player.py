import random as rand
from Game import Game
from copy import deepcopy
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

class MinimaxPlayer:
    def __init__(self, depth=3, player_num=1):
        self.depth = depth
        self.player_num = player_num

    def get_move(self, game, player_hand):
        # Example usage of simulate_move
        new_game_state = game.simulate_move("hit")  # Simulate a 'hit'
        # Assess the new game state to decide the next move...

        # Use some criteria or minimax logic here to determine the move
        return self.minimax(game.copy(), player_hand, self.depth)

    # def minimax_decision(self, game, player_hand):
    #     best_move = None
    #     best_score = float('-inf')
    #     legal_moves = self.get_legal_moves(game)

    #     # Simulate each legal move and calculate the minimax score
    #     for move in legal_moves:
    #         # You need to update game state based on move, this part is missing
    #         new_game_state = self.simulate_move(game, player_hand, move)
    #         score = self.minimax(new_game_state, move, depth=10)  # Assuming depth starts at 3
    #         if score > best_score:
    #             best_score = score
    #             best_move = move

    #     return best_move

    # def simulate_move(self, game, player_hand, move):
    #     # Create a deep copy of the game state to modify
    #     # Note: You'll need to ensure Game class supports cloning or copying
    #     new_game_state = deepcopy(game)  # This requires 'from copy import deepcopy'
    #     # Apply the move to the new game state
    #     new_game_state.apply_move(player_hand, move)  # You need to implement this method in Game
    #     return new_game_state

    def minimax(self, game_state, move, depth):
        if depth == 0 or game_state.winner is not None:
            return self.evaluate(game_state)

        if game_state.turn == self.player_num:  # Player's turn (e.g., you in Blackjack)
            best_score = float('-inf')
            for next_move in self.get_legal_moves(game_state):
                if next_move == "hit":
                    game_state.hit()
                else:
                    game_state.stand()
                score = self.minimax(game_state, next_move, depth - 1)
                best_score = max(best_score, score)
            return best_score
        else:  # Opponent's turn (e.g., dealer in Blackjack)
            best_score = float('inf')
            for next_move in self.get_legal_moves(game_state):
                if next_move == "hit":
                    game_state.hit()
                else:
                    game_state.stand()
                score = self.minimax(game_state, next_move, depth - 1)
                best_score = min(best_score, score)
            return best_score

    def evaluate(self, game_state):
        player_score = game_state.calculateScore(game_state.board[self.player_num])
        dealer_card = game_state.calculateScore(game_state.board[0])  # Assume only the dealer's visible card matters
        remaining_cards = game_state.deck
        
        if player_score > 21:
            return -float('inf')  # Assign a very low score if player busts.
        
        # Base score is primarily the player's current hand value normalized.
        score = player_score - 21 if player_score <= 21 else -100  # Punish going over 21.

        # Modify score based on dealer's card.
        if dealer_card >= 7:
            score -= 5  # More risky situation if dealer has a strong card.
        elif dealer_card <= 6:
            score += 5  # Less risk if dealer might bust.

        # Adjust score based on the distribution of remaining cards.
        favorable_cards = sum(1 for card in remaining_cards if game_state.calculateScore([card]) + player_score <= 21)
        total_cards = len(remaining_cards)
        bust_probability = (total_cards - favorable_cards) / total_cards if total_cards else 1

        # Adjust score based on bust probability.
        score -= bust_probability * 10  # Penalize high risk of busting.
        return score

    def get_legal_moves(self, game_state):
        moves = ['stand', 'hit']  # Basic moves available in every situation.

        # Check conditions for double down or split (if your rules allow these moves)
        # Example: Player can double down only on certain hand values (like 9, 10, 11).
        # if game_state.can_double_down():
        #     moves.append('double down')
        # if game_state.can_split():
        #     moves.append('split')

        return moves
