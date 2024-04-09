from Player import *

# Test the Player class
if __name__ == "__main__":
    manual_player = ManualPlayer()
    random_player = RandomPlayer()
    dealer = Dealer()

    # [Dealer, Player 1, Player 2, ...]
    players = [dealer, manual_player, random_player]

    game = Game(len(players), decks=1)
    # game.play_game(players)
    
    
    
    # Test the multiGame function,
    # multiGame(players, num_games, printOutput=True, againstDealer=True)
    players = [dealer, random_player, random_player]
    print(game.multiGame(players, 1000, True, False))