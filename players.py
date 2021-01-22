"""Players for the switch game."""
import random
import user_interface as ui


class Player:
    """Player class for a human player."""
    is_ai = False

    def __init__(self, name):
        self.name = name
        self.hand = []

    @staticmethod
    def select_card(choices, _):
        """Select a card to be discarded.

        Delegates choice to user_interface.
        """
        return ui.select_card(choices)

    @staticmethod
    def ask_for_swap(others):
        """Select a player to switch hands with.

        Delegates choice to user_interface.
        """
        return ui.select_player(others)

    @staticmethod
    def select_card_option(card):
        """Select an option of what to do with
        a card that was drawn after nothing was discarded.

        Delegates choice to user_interface.
        """
        return ui.select_discard_choice(card)


class SimpleAI:
    """Simple computer strategy.

    This AI player performs random decisions.
    """
    is_ai = True

    def __init__(self, name):
        self.name = name
        self.hand = []

    def select_card(self, choices, _):
        """Select a card to be discarded.

        Randomly chooses one of the valid choices
        including a choice not to discard a card.
        """
        choices.append("No discard")
        choice = random.choice(choices)
        if choice == "No discard":
            return False
        else:
            return choice

    def ask_for_swap(self, others):
        """Select a player to swap hands with.

        Randomly chooses one of the players.
        """
        return random.choice(others)

    def select_card_option(self, card, others):
        """Select an option of what to do with
        a card that was drawn after nothing was discarded.

        Randomly chooses one of the options.
        """
        discard_card = random.choice([True, False])
        return discard_card


class SmartAI(SimpleAI):
    """Smart computer strategy.

    This AI player makes choices based on the
    current game state.
    """
    def select_card(self, choices, hands):
        """Select a card to be discarded.

        Selects a card that either harms opponents or
        chooses a suit that the player holds the most cards of.
        """
        def score(card):
            in_suit = len([c for c in self.hand
                           if c.suit == card.suit and c is not card])

            offset = {
                'J': 3*(hands[0]-1-min(hands[1:])),
                'Q': 6 + in_suit,
                '2': 4 + in_suit,
                '8': 2 + in_suit,
                'K': (3 if hands[-1] > hands[1] else -1) + in_suit,
                'A': -2 + in_suit,
            }

            return offset.get(card.value, in_suit)
        sorted_choices = sorted(choices, key=score, reverse=True)
        candidate = sorted_choices[0]
        if score(candidate) > -2:
            return candidate if score(candidate) > -2 else None

    def ask_for_swap(self, others):
        """Select a player to swap hands with.

        Switch hands with the player who holds the least cards.
        """
        smallest = min(len(p.hand) for p in others)
        best = [p for p in others if len(p.hand) == smallest]
        return random.choice(best)

    def select_card_option(self, card, others):
        """Select an option of what to do with
        a card that was drawn after nothing was discarded.

        Choose to add card to hand if it would be useful in the future
        or harm the player, otherwise discard.
        """
        # Variables that help determining whether to discard or not.
        same_suit = len([c for c in self.hand if c.suit == card.suit and c is not card])
        different_suits = {c.suit for c in self.hand if c is not card}
        qa_in_hand = len([c for c in self.hand if c.value in 'QA' and c is not card])
        smallest = min(len(p.hand) for p in others)

        # If the player has more than 1 card in hand,
        if len(self.hand) >= 2:
            # If the player doesn't have some card suit in hand,
            if len(different_suits) < 4:
                # If card's value is Q or A and player has no Q or A in hand, add it to hand.
                if card.value in 'QA' and qa_in_hand == 0:
                    return False
                # If player doesn't have cards with drawn card's suit in hand, add it to hand.
                elif same_suit == 0:
                    return False
                # Otherwise discard.
                else:
                    return True
            # If the drawn card is a J and the player's hand is the smallest, add it to hand.
            elif card.value == 'J' and len(self.hand) < smallest:
                return False
            # Otherwise discard.
            else:
                return True
        # If the drawn card is a J,
        elif card.value == 'J':
            # If the player's hand is the smallest, add it to hand.
            if len(self.hand) < smallest:
                return False
            # Otherwise discard.
            else:
                return True
        # If the player has 1 remaining card in hand and the drawn card is not a J, discard.
        else:
            return True


player_classes = {
    'human': Player,
    'simple': SimpleAI,
    'smart': SmartAI,
}
