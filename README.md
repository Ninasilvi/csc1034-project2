# Switch

Switch is a card game similar to the popular UNO game. The objective
of the game is to be the first player who discards all their cards. 
Some cards have effects when discarded, resulting in consequences on 
the subsequent player or the flow of the game.

## Rules

Switch is played by 2-4 players. Each player is initially dealt a hand
of seven cards. The stock pile of remaining cards is put on the table face down. 
One card is taken from the stock pile and placed face up to initiate the discard pile.

Players take turns in discarding cards from their hand. A card can be 
discarded if it matches the top-most card of the discard pile (top card) 
in either the suit (diamond, hearts, clubs, or spade) or the value. 
In addition, aces and queens can always be discarded despite what the 
current top card is.

Some cards have special effects:

| Card  | Discard Rule       | Effect                                                                             |
| :---: | ------------------ | -----------------------------------------------------------------------------------|
| 2     | Same suit or value | Next player must draw two cards from the stock pile at the beginning of their turn |
| 8     | Same suit or value | Next player is skipped and the game proceeds with the subsequent player's turn     |
| J     | Same suit or value | The player must swap their hand with the hand of another player                    |
| Q     | Anytime            | Next player must draw four cards from the stock pile at the beginning of their turn|
| K     | Same suit or value | The direction of the game changes before the start of next player's turn           |
| A     | Anytime            | None                                                                               |

If a player is unable to discard any cards or chooses not to discard, they must 
draw a card from the stock pile. If that card can be discarded, the player 
must do so immediately, otherwise the card goes into the player's hand and the game
proceeds with the next player.

If there are no more cards in the stock pile, all discards except for the 
top card are shuffled and placed face down to form a new stock pile.


## Running the game

Start Switch in the terminal with

	$ python3 switch.py

Or press `Run` in your IDE.

Run the test suite with

	$ python3 -m pytest

The latter assumes that you have installed pytest using

    $ pip3 install pytest
