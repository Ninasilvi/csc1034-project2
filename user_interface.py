"""Command line interface for the switch game."""
import random


def print_message(msg):
    """Print out a message to UI."""
    print(msg)


def say_welcome():
    """Print a welcome message."""
    print_message("Welcome to Switch v1.3.2")


def print_game_menu():
    """Display game menu."""
    print_message("\nPlease select from one of the following options: [1-2]")
    print_message("1 - New Game")
    print_message("2 - Exit")


def print_player_info(player, top_card, index, direction):
    """Display player information and public game state."""
    print_message(f"\nPLAYER: {index}")
    print_message(f"HAND SIZE: {len(player.hand)}")
    print_message(f"GAME DIRECTION: {direction}")
    print_message(f"PLAYER: {player.name}")
    if not player.is_ai:
        print_message("HAND: " + ", ".join(str(card) for card in player.hand))
    print_message(f"TOP CARD: {top_card}")


def print_discard_result(discarded, card):
    """Display a discard message."""
    if discarded:
        print_message(f"Discarded: {card}\n")
    else:
        print_message(f"Unable to discard card: {card}\n")


def print_winner_of_game(player):
    """Display winner information."""
    print_message('\n'+80*'-')
    print_message(f"Woohoo!!! Winner of the game is: {player.name}")
    print_message(80*'-')


def say_goodbye():
    """Print a goodbye message."""
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
            print_message(f"Try again: Input should be an integer between [{min_val:d}-{max_val:d}]")
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
    print_message("\nHow many human players [1-4]:")
    no_of_players = get_int_input(1, max_players)

    # Get the names of each human player.
    for i in range(no_of_players):
        print_message(f"\nPlease enter the name of player {i+1}:")
        player_info.append(('human', get_string_input()))

    ai_names = ["Angela", "Bart", "Charly", "Dorothy", "John", "Paul", "Ringo", "George"]
    # Determine minimum and maximum values of AI players. Ensures there's at least 2 players.
    min_val = 1 if (len(player_info) <= 1) else 0
    max_val = max_players - no_of_players
    print_message(f"\nHow many AI players [{min_val:d}-{max_val:d}]:")
    no_of_players = get_int_input(min_val, max_val)

    # Starting number for while loop.
    num = 0
    # Randomly assign AI players.
    while num < no_of_players:
        # Picks a random AI name and removes it from the name list to avoid repetition.
        name = random.choice(ai_names)
        ai_names.remove(name)
        # Randomly assign simple AI or smart AI strategy.
        ai_type = random.choice([True, False])
        if ai_type:
            player_info.append(('simple', name))
        else:
            player_info.append(('smart', f"Smart {name}"))
        # Number for while loop increases by one with each iteration.
        num += 1
    return player_info


def select_card(cards):
    """Select a card from the hand or choose not to discard."""
    print_message(f"Please select from one of the following cards: [1-{len(cards):d}]\n"
                  f"If you would like not to discard this turn, select: [{len(cards)+1}]")
    for i in range(len(cards)):
        card = cards[i]
        print_message(f"{i+1} - {card}")
    print_message(f"{len(cards)+1} - No discard")

    # Get a card choice and return the card.
    choice = get_int_input(1, len(cards)+1)
    if choice == len(cards)+1:
        return False
    return cards[choice-1] if choice else None


def select_player(players):
    """Select another player."""
    print_message(f"Please select from one of the following players: [1-{len(players):d}]")
    # Print out a list of all other players.
    for idx, player in enumerate(players):
        print_message(f"{idx + 1:d} - {player.name} = {len(player.hand):d}")

    # Get a player choice and return the player.
    choice = get_int_input(1, len(players))
    return players[choice - 1]


def select_discard_choice(card):
    """Display options for the card drawn when nothing was discarded."""
    print_message(f"\nCard drawn: {card}")
    print_message("Please select what you would like to do with this card: [1-2]")
    print_message("1 - Discard")
    print_message("2 - Add to hand")
    choice = get_int_input(1, 2)
    if choice == 1:
        return True
    elif choice == 2:
        print_message(f"{card} has been added to hand.")
        return False
