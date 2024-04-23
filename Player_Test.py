from Player import *
import matplotlib.pyplot as plt

# Test the Player class
if __name__ == "__main__":
    
    

    # [Dealer, Player 1, Player 2, ...]
    players = [Dealer(), RandomPlayer(), MinimaxPlayer()]

    game = Game(len(players), decks=1)
    # game.play_game(players)
    
    
    # Test the multiGame function,
    # multiGame(players, num_games, printOutput=True, againstDealer=True)

    players = [Dealer(), NearestNeighborPlayer(), MinimaxPlayer(player_num=2)]
    num_games = 1000
    
    # this is used later to plot the results
    wins = game.multiGame(players, num_games, againstDealer=True)
    print(wins)
    
    
    
    
    # Define the data
    player_names = [player.__class__.__name__ for player in players]

    player_wins = [0] * len(players)
    player_ties = [0] * len(players)
    player_losses = [0] * len(players)

    for i in range(len(players)):
        player_wins[i] = wins[i][0]
        player_ties[i] = wins[i][1]
        player_losses[i] = num_games - (wins[i][0] + wins[i][1])

    # Set up the figure and axis
    fig, ax = plt.subplots()

    # Set the bar width
    bar_width = 0.25

    # Set the x-axis positions for the bars
    r1 = range(len(players))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width * 2 for x in r1]

    # Plot the bars
    ax.bar(r1, player_losses, width=bar_width, label='Losses', color='r')
    ax.bar(r2, player_wins, width=bar_width, label='Wins', color='g')
    ax.bar(r3, player_ties, width=bar_width, label='ties', color='b')

    # Add labels and title
    ax.set_xticks([r + bar_width for r in range(len(players))])
    ax.set_xticklabels(player_names)
    ax.set_ylabel('Counts')
    ax.set_title('Blackjack Game Results')
    ax.legend()

    # Show the plot
    plt.show()