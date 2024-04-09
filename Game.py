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
        # check if the number of players and decks are valid
        VALIDPLAYERS = range(2, 8)
        VALIDDECKS = range(1, 5)
        if players not in VALIDPLAYERS or decks not in VALIDDECKS:
            raise ValueError("Invalid number of players or decks.")
         
         
        # initalize the board
        self.values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        self.board = []
        self.turn = 1
        self.winner = None
        self.moves = 0
        self.players = []
        self.decksNum = decks
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


    def resetGame(self):
        self.deck = self.initalizeDeck(self.decksNum)
        self.shuffleDeck()
        self.board = []
        self.turn = 1
        self.winner = None
        self.moves = 0
        for i in range(len(self.players)):
            self.players[i] = []
            
        
    def hit(self, printOutput = True):
        if self.turn == 0:
            print("Game has ended. No more moves allowed.")
            return
        self.players[self.turn - 1].append(self.deck.pop())
        self.board[self.turn - 1].append(self.players[self.turn - 1][-1])
        self.moves += 1
        if self.checkBust():
            self.nextTurn(printOutput)
    
    def stand(self, printOutput = True):
        if self.turn == 0:
            print("Game has ended. No more moves allowed.")
            return
        self.nextTurn(printOutput)

    # moves to the next turn, if the dealer's turn reveal the hidden card
    def nextTurn(self, printOutput = True):
        if self.turn == 1 and self.moves >= len(self.players) - 1:
            # It's the dealer's turn
            self.board[0][1] = self.players[0][1]  # Reveal the dealer's hidden card
            if printOutput:
                print(f"Dealer's turn. Hand: {self.players[0]}")
        
        self.turn += 1
        if self.turn > len(self.players):
            self.turn = 1

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
    def play_game(self, players, againstDealer = True):
        # Check if the number of players is valid
        if len(players) != len(self.players):
            raise ValueError("Invalid number of players.")
        
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
                    move = player.get_move(self, player_hand)  # Get the player's move

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
                move = players[0].get_move(self, dealer_hand)

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
                
            self.endGame(againstDealer=againstDealer)
            break

        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again == 'y':
            self.__init__(len(players), self.decksNum)
            self.play_game(players)
        else:
            print("Thanks for playing!")
    
    # Plays multiple games and returns the number of wins for each player, 
    # and the number of ties at the end
    def multiGame(self, players, games, printOutput = True, againstDealer = True):
        wins = [0] * (len(players) + 1)
        
        # Check if the number of players is valid
        if len(players) != len(self.players):
            raise ValueError("Invalid number of players.")
        
        for i in range(games):
            
            self.resetGame()
            self.dealCards()
            if printOutput:
                print(f"\nGame {i + 1}")
            
            while True:
                for player_idx, player in enumerate(players):
                    if player_idx == 0:  # Dealer's turn
                        continue

                    self.turn = player_idx + 1
                    player_hand = self.players[player_idx]

                    while self.calculateScore(player_hand) < 21:
                        move = player.get_move(self, player_hand)  # Get the player's move

                        if move == "hit":
                            self.hit(printOutput)
                        elif move == "stand":
                            break
                        else:
                            break

                        if self.checkBust():
                            break

                # Dealer's turn
                self.turn = 1
                dealer_hand = self.players[0]

                while self.calculateScore(dealer_hand) < 21:  # Dealer hits until their score reaches 17 or more
                    move = players[0].get_move(self, dealer_hand)

                    if move == "hit":
                        self.hit(printOutput)
                    elif move == "stand":
                        break
                    else:
                        break

                    if self.checkBust():
                        break
                    
                self.endGame(printOutput, againstDealer)
                
                if self.winner is not None:
                    if len(self.winner) >= 1:
                        for winner in self.winner:
                            wins[winner] += 1
                    else:
                        wins[-1] += 1
                break
                
        return wins

    
    # ends the game and determines the winner
    def endGame(self, printOutput=True, againstDealer=True):
        # Calculate scores for all players
        scores = []
        playerScores = []
        dealerScore = self.calculateScore(self.players[0])
        for player in self.players:
            score = self.calculateScore(player)
            scores.append(score)
            playerScores.append(score)
        
        
        # Determine the winner(s)
        winners = []
        if againstDealer:
            for i in range(1, len(scores)):
                if scores[i] > 21:
                    continue
                if scores[i] > scores[0] or scores[0] > 21:
                    winners.append(i)
            if len(winners) == 0 and scores[0] <= 21:
                winners.append(0)
        else: # Against each other
            maxScore = 0
            winner = None
            for i in range(len(scores)):
                if scores[i] >= maxScore and scores[i] <= 21:
                    maxScore = scores[i]
                    winner = i
            if winner is not None:
                winners.append(winner)
        

        self.turn = 0  # Game over
        self.winner = winners
        # Print the game result if required
        if printOutput:
            
            print(f"\nFinal Board: {self.players}")
            print(f"Scores: {scores}")
            if againstDealer:
                print(f"Dealer's hand: {self.players[0]}")
            
            if len(winners) == 1 and winners[0] != 0:
                print(f"Player {winners[0]} wins!")
            elif len(winners) > 1:
                print("Winners are: ", self.winner)
            elif len(winners) == 1 and winners[0] == 0:
                print("Dealer wins!")
            else:
                print("Tie game!")
                
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
    