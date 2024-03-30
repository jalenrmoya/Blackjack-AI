import random as rand

# BlackJack Game Class
class Game:
    # players: number of players
    # decks: number of decks the more decks the more cards
    # board = [dealer's cards, player1's cards, player2's cards, ...]
    # turn: current player's turn dealer = 0, player1 = 1, player2 = 2, ...
    # winner: the winner of the game (winner = turn of winner)
    # moves = number of moves made in the game
    def __init__(self, players = 2, decks = 1):
        # initalize the board
        self.values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        self.board = []
        self.turn = 1
        self.winner = None
        self.moves = 0
        self.players = []
        for i in range(players):
            self.players.append([])

        # initalize the deck and shuffle 
        self.deck = self.initalizeDeck(decks)
        self.shuffleDeck()



    # initalizes the deck of cards using the number of decks
    # and shuffles the deck
    def initalizeDeck(self, decks = 1):
        cards = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        suits = ['spades', 'hearts', 'diamonds', 'clubs']
        deck = []
        for i in range(decks):
            for suit in suits:
                for card in cards:
                    deck.append(card)
        return deck
    
    def shuffleDeck(self):
        rand.shuffle(self.deck)
        return self.deck
    
    # deals the cards to the players
    # 2 cards per player and dealers second card is hidden
    def dealCards(self):
        for i in range(2):
            for player in self.players:
                player.append(self.deck.pop())

        self.board = [list(player) for player in self.players]
        self.board[0][1] = '🂠'


    def hit(self):
        if self.turn == 0:
            print("Game has ended. No more moves allowed.")
            return
        self.players[self.turn - 1].append(self.deck.pop())
        self.board[self.turn - 1].append(self.players[self.turn - 1][-1])
        self.moves += 1
        if self.checkBust():
            self.nextTurn()
    
    def stand(self):
        if self.turn == 0:
            print("Game has ended. No more moves allowed.")
            return
        self.nextTurn()

    # moves to the next turn, if the dealer's turn reveal the hidden card
    def nextTurn(self):
        if self.turn == 1 and self.moves >= len(self.players) - 1:
            # It's the dealer's turn
            self.board[0][1] = self.players[0][1]  # Reveal the dealer's hidden card
            print(f"Dealer's turn. Hand: {self.players[0]}")
        self.turn += 1
        if self.turn > len(self.players):
            self.turn = 1
        if self.moves >= len(self.players):
            self.endGame()

    # checks if the player has busted
    def checkBust(self):
        return self.calculateScore(self.players[self.turn - 1]) > 21
    
    # calculates the score of the player based on the cards
    def calculateScore(self, player):
        score = 0
        aces = 0
        for card in player:
            if card == 'A':
                aces += 1
            score += self.values[card]
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score
    
    # Is given a list of Players from the Player class and uses their moves to play the game
    # player = [Dealer, Player 1, Player 2, ...]
    def play_game(self, players):
        self.dealCards()
        print("Initial Board: ", self.getBoard())

        while True:
            for player_idx, player in enumerate(players):
                if player_idx == 0:  # Dealer's turn
                    continue

                self.turn = player_idx + 1
                player_hand = self.players[player_idx]
                print(f"\nPlayer {player_idx}'s turn. Hand: {player_hand}")

                while self.calculateScore(player_hand) < 21:
                    move = player.get_move(self)  # Get the player's move

                    if move == "hit":
                        self.hit()
                        print(f"Player {player_idx}'s hand: {player_hand}")
                    elif move == "stand":
                        break
                    else:
                        print("Invalid move. Skipping player's turn.")
                        break

                    if self.checkBust():
                        print(f"Player {player_idx} busted with hand: {player_hand}")
                        break

            # Dealer's turn
            self.turn = 1
            dealer_hand = self.players[0]
            print(f"\nDealer's turn. Hand: {dealer_hand}")

            while self.calculateScore(dealer_hand) < 21:  # Dealer hits until their score reaches 17 or more
                move = players[0].get_move(self)

                if move == "hit":
                    self.hit()
                    print(f"Dealer's hand: {dealer_hand}")
                elif move == "stand":
                    break
                else:
                    print("Invalid move. Skipping dealer's turn.")
                    break

                if self.checkBust():
                    print(f"Dealer busted with hand: {dealer_hand}")
                    break
                
            self.endGame()
            break

        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again == 'y':
            self.__init__(len(players), self.decksNum)
            self.play_game(players)
        else:
            print("Thanks for playing!")
    
    # ends the game and determines the winner
    def endGame(self):
        maxScore = 0
        for i in range(1, len(self.players)):  # Start from 1 to exclude the dealer
            score = self.calculateScore(self.players[i])
            if score > maxScore and score <= 21:
                maxScore = score
                self.winner = i

        dealerScore = self.calculateScore(self.players[0])
        if dealerScore > maxScore and dealerScore <= 21:
            self.winner = 0

        self.turn = 0  # game over
        if self.winner is not None:
            print("Board: ", self.players)
            if self.winner == 0:
                print(f"Winner is: Dealer with the hand ", self.players[self.winner])
                print("Score: ", dealerScore)
            else:
                print(f"Winner is: Player {self.winner} with the hand ", self.players[self.winner])
                print("Score: ", maxScore)
        else:
            print("Tie Game!")
            print("Board: ", self.board)


    # returns the current player
    def currentPlayer(self):
        return self.players[self.turn - 1]
    # returns the current turn
    def getTurn(self):
        return self.turn
    
    # returns the current players
    def getPlayers(self):
        return self.players
    
    # returns the current board 
    def getBoard(self):
        return self.board
    