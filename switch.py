"""Main module of the switch game."""
import random
from players import player_classes
import user_interface as ui

from cards import generate_deck


# Set the constant game values.
MAX_PLAYERS = 4
HAND_SIZE = 7


class Switch:
    """The Switch game.

    To run the game, a Switch object is created and its run_game method is called.

    Switch objects have the following attributes, which are initialized
    by the Switch.setup_round method:

    self.players - list of Player objects;
    self.stock - list of cards to draw from;
    self.discards - list of discarded cards;
    self.skip - bool indicating that the next player is skipped;
    self.draw2 - bool indicating that the next player must draw 2 cards;
    self.draw4 - bool indicating that the next player must draw 4 cards;
    self.direction - int, either 1 or -1, indicating the direction of the game.
    """
    def __init__(self):
        self.players = []
        self.stock = []
        self.discards = []
        self.skip = False
        self.draw2 = False
        self.draw4 = False
        self.direction = 1

    def run_game(self):
        """Run rounds of the game until player decides to exit."""
        ui.say_welcome()
        # Show game menu and run rounds if the input is 1.
        while True:
            ui.print_game_menu()
            choice = ui.get_int_input(1, 2)
            if choice == 1:
                # Set up self.players before the round starts.
                player_info = ui.get_player_information(MAX_PLAYERS)
                self.players = [player_classes[typ](name) for typ, name in player_info]
                self.run_round()
            # If the input is 2, exit the game and print goodbye message.
            else:
                break
        ui.say_goodbye()

    def run_round(self):
        """Run a single round of Switch.

        Continuously calls run_player method for the current player,
        and advances the current player depending on the current game direction.
        """
        # Deal cards and set up game round.
        self.setup_round()

        # Current player index.
        i = 0
        while True:
            # Run current player's turn.
            self.run_player(self.players[i])
            # Check if the player's hand is empty - if it is, they won and the game ends.
            won = not self.players[i].hand
            if won:
                ui.print_winner_of_game(self.players[i])
                break
            # If the player didn't win, the game progresses to the next player based on the game's direction.
            else:
                if i == len(self.players) - 1 and self.direction == 1:
                    i = 0
                elif i == 0 and self.direction == -1:
                    i = len(self.players) - 1
                else:
                    i = i + self.direction
                continue

    def setup_round(self):
        """Initialize a round of Switch.

        Sets the stock to a full shuffled deck of cards, initializes
        the discard pile with its first card, deals all players their
        hands and sets game flags to their initial values.
        """
        # Shuffle deck of cards and initialize discard pile with a top card.
        self.stock = generate_deck()
        random.shuffle(self.stock)
        self.discards = [self.stock.pop()]
        # Deal hands.
        for player in self.players:
            self.pick_up_card(player, HAND_SIZE)
        # Set game flags to initial values.
        self.direction = 1
        self.skip = False
        self.draw2 = False
        self.draw4 = False

    def run_player(self, player):
        """Process a single player's turn.

        Parameters:
        player - Player to make the turn.

        Returns True if someone has won within his turn, otherwise False.

        In each turn, game effects are applied according to the outcome of the last turn.
        The player is then asked to select a card via a call to Player.select_card which is then discarded
        via a call to discard_card. If the player has no discardable card (or chooses not to discard),
        draw_and_discard is called to draw from stock.
        """
        # Apply any pending penalties (skip, draw2, draw4).
        if self.skip:
            self.skip = False
            ui.print_message('{} is skipped.'.format(player.name))
            return False

        if self.draw2:
            picked = self.pick_up_card(player, 2)
            self.draw2 = False
            ui.print_message('{} draws {} cards.'.format(player.name, picked))

        if self.draw4:
            picked = self.pick_up_card(player, 4)
            self.draw4 = False
            ui.print_message('{} draws {} cards.'.format(player.name, picked))

        top_card = self.discards[-1]
        player_index = self.players.index(player) + 1
        direction = "Clockwise" if self.direction == 1 else "Anti-clockwise"
        ui.print_player_info(player, top_card, player_index, direction)

        # Determine discardable cards.
        discardable = []
        for card in player.hand:
            if not self.can_discard(card):
                continue
            discardable.append(card)

        # Have the player select a card.
        hands = self.get_normalized_hand_sizes(player)
        card = player.select_card(discardable, hands) if discardable else None

        if card:
            # Discard a card and determine whether the player has won.
            self.discard_card(player, card)
            return not player.hand
        # Draw a card and discard if eligible.
        if discardable:
            # If the player has chosen not to discard, change the no_discard parameter to True.
            self.draw_and_discard(player, True)
        else:
            self.draw_and_discard(player, False)
        return False

    def can_discard(self, card):
        """Return whether a card can be discarded."""
        # Q and A can always be discarded.
        if card.value in 'QA':
            return True
        # Otherwise either suit or value has to match with the top card.
        top_card = self.discards[-1]
        return card.suit == top_card.suit or card.value == top_card.value

    def pick_up_card(self, player, amount=1):
        """Pick up a card from stock and add to player hand.

        Parameters:
        player - Player who picks the card.

        Keyword arguments:
        amount - number of cards to pick (default 1).

        Returns the number of cards picked.

        Picks n cards from the stock pile and adds it to the player's
        hand. If the stock has less than n cards, all but the top most
        discard are shuffled back into the stock. If this is still not
        sufficient, the maximum possible number of cards is picked.
        """
        for i in range(1, amount+1):
            # If there are no more cards in the stock pile.
            if not self.stock:
                if len(self.discards) == 1:
                    ui.print_message("All cards distributed")
                    return i-1
                # Add back discarded cards excluding the top card.
                self.stock = self.discards[:-1]
                del self.discards[:-1]
                random.shuffle(self.stock)
                ui.print_message("Discards are shuffled back.")
            # Draw a stock card and append it to player's hand.
            card = self.stock.pop()
            player.hand.append(card)
            if i == amount:
                return i
            else:
                continue

    def discard_card(self, player, card):
        """Discard a card and apply its game effects.

        Parameters:
        player - Player who discards card;
        card - Card to be discarded.
        """
        # Remove card from player's hand and add it to discard pile.
        player.hand.remove(card)
        self.discards.append(card)
        ui.print_discard_result(True, card)
        # If the player's hand is empty, the player won.
        if not player.hand:
            return
        # If card is an 8, skip the next player.
        if card.value == '8':
            self.skip = True
        # If card is a 2, next player needs to draw 2.
        elif card.value == '2':
            self.draw2 = True
        # If card is a Q, next player needs to draw 4.
        elif card.value == 'Q':
            self.draw4 = True
        # If card is a K, game direction reverses.
        elif card.value == 'K':
            self.direction *= -1
            ui.print_message("Game direction reversed.")
        # If card is a J, ask player with whom to swap hands.
        elif card.value == 'J':
            others = [p for p in self.players if p is not player]
            choice = player.ask_for_swap(others)
            self.swap_hands(player, choice)

    def draw_and_discard(self, player, no_discard=False):
        """Draw a card from stock and ask whether the player wants to
        discard it if possible.

        Parameters:
        player - Player that draws the card.
        no_discard - A boolean value that shows whether the player has chosen not to
            discard a card this turn (default False).

        Calls pick_up_card to obtain a stock card and adds it to the
        player's hand. If the card can be discarded, discard_card method is
        called with the newly picked card.
        """
        # Print out a message depending on whether the player chose not to discard or had no discardable cards.
        if no_discard:
            ui.print_message(f"{player.name} has chosen not to discard. Drawing ...")
        else:
            ui.print_message("No matching card. Drawing ...")
        # Return if no card could be picked.
        if not self.pick_up_card(player):
            return
        # Discard picked card if possible.
        card = player.hand[-1]
        # AIs choose whether to discard (if possible) based on strategy and circumstances.
        if self.can_discard(card) and player.is_ai:
            others = [p for p in self.players if p is not player]
            choice = player.select_card_option(card, others)
            if choice:
                self.discard_card(player, card)
            else:
                player.hand.append(card)
                ui.print_message(f"{player.name} has chosen to add the card to their hand.")
        # Human players are asked whether they want to discard the card (if possible).
        elif self.can_discard(card) and not player.is_ai:
            choice = player.select_card_option(card)
            if choice:
                self.discard_card(player, card)
            else:
                player.hand.append(card)
        # Inform the player if the card could not be discarded.
        elif not player.is_ai:
            ui.print_discard_result(False, card)
        elif player.is_ai:
            ui.print_message("Card cannot be discarded.")

    def get_normalized_hand_sizes(self, player):
        """Return list of hand sizes in normal form.

        Parameter:
        player - Player for whom to normalize view.

        Returns a list of integers of player sample length.

        The list of hand sizes is rotated and flipped so that the
        specified player is always at position 0 and the next player
        (according to current direction of play) at position 1.
        """
        sizes = [len(p.hand) for p in self.players]
        idx = self.players.index(player)
        # Rotate list so that given player is first.
        sizes = sizes[idx:] + sizes[:idx]
        # If direction is counter-clockwise.
        if self.direction == -1:
            # Reverse the order and bring given player back to the front.
            sizes.reverse()
            sizes.insert(0, sizes.pop())
        return sizes

    @staticmethod
    def swap_hands(player_1, player_2):
        """Exchanges the hands of the two given players."""
        player_1.hand, player_2.hand = player_2.hand, player_1.hand
        ui.print_message(f"{player_1.name} swaps hands with {player_2.name}.")


if __name__ == '__main__':
    game = Switch()
    game.run_game()
