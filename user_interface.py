"""Command line interface for the switch game."""
import random


def print_message(msg):
    """Print out a message to UI."""
    print(msg)


def say_welcome():
    """Print a welcome message."""
    print_message("Welcome to Switch v1.2.0")


def print_game_menu():
    """Display game menu."""
    print("\nPlease select from one of the following options: [1-2]")
    print("1 - New Game")
    print("2 - Exit")


def print_player_info(player, top_card, hands):
    """Display player information and public game state."""
    print(f"\nHANDS: {hands}")
    print(f"PLAYER: {player.name}")
    if not player.is_ai:
        print("HAND: " + ", ".join(str(card) for card in player.hand))
    print(f"TOP CARD: {top_card}")


def print_discard_result(discarded, card):
    """Display a discard message."""
    if discarded:
        print(f"Discarded: {card}\n")
    else:
        print(f"Unable to discard card: {card}")


def print_winner_of_game(player):
    """Display winner information."""
    print_message('\n'+80*'-')
    print_message(f"Woohoo!!! Winner of the game is: {player.name}")
    print_message(80*'-')


def say_goodbye():
    """Say goodbye to my little friend."""
    print_message("Goodbye!")


def convert_to_int(string):
    """Convert string to int."""
    result = -1
    try:
        result = int(string)
    except ValueError:
        pass
    return result


def get_int_input(min_val, max_val):
    """Get int input from the user."""
    choice = -1
    while choice < min_val or choice > max_val:
        print("> ", end="")
        choice = convert_to_int(input())
        if choice < min_val or choice > max_val:
            print(f"Try again: Input should be an integer between [{min_val:d}-{max_val:d}]")
    return choice


def get_string_input():
    """Get string input from the user."""
    print("> ", end="")
    return input()


def get_player_information(max_players):
    """Get required information to set up a round."""
    # Create a player info list.
    player_info = []
    # Get input of the number of human players.
    print("\nHow many human players [1-4]:")
    no_of_players = get_int_input(1, max_players)

    # Get the names of each human player.
    for i in range(no_of_players):
        print(f"Please enter the name of player {i+1}:")
        player_info.append(('human', get_string_input()))

    ai_names = ["Angela", "Bart", "Charly", "Dorothy", "John", "Paul", "Ringo", "George"]
    # Determine minimum and maximum values of AI players. Ensures there's at least 2 players.
    min_val = 1 if (len(player_info) <= 1) else 0
    max_val = max_players - no_of_players
    print(f"\nHow many ai players [{min_val:d}-{max_val:d}]:")
    no_of_players = get_int_input(min_val, max_val)

    # Starting umber for while loop.
    num = 0
    # Randomly assign AI players.
    while num < no_of_players:
        # Picks a random AI name and removes it from the name list to avoid repetition.
        name = random.choice(ai_names)
        ai_names.remove(name)
        # Randomly assigns simple AI or smart AI strategy.
        ai_type = random.choice([True, False])
        if ai_type:
            player_info.append(('simple', name))
        else:
            player_info.append(('smart', f"Smart {name}"))
        # Number for while loop increases by one with each iteration.
        num += 1
    return player_info


def select_card(cards):
    """Select a card from a hand."""
    print(f"Please select from one of the following cards: [1-{len(cards):d}]")
    for i in range(len(cards)):
        card = cards[i]
        print(f"{i+1} - {card}")

    # Get a card choice and return the card.
    choice = get_int_input(1, len(cards))
    return cards[choice-1] if choice else None


def select_player(players):
    """Select another player."""
    print(f"Please select from one of the following players: [1-{len(players):d}]")
    # Print out a list of all other players.
    for idx, player in enumerate(players):
        print(f"{idx + 1:d} - {player.name} = {len(player.hand):d}")

    # Get a player choice and return the player.
    choice = get_int_input(1, len(players))
    return players[choice - 1]
