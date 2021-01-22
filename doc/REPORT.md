# Report

## Strategies used to find errors in code base

### Debugging

When working on this project, I predominantly used the debugger to find and fix bugs. I started by running 
the code to find the source of the error stated in traceback and put breakpoints on the line
in question, as well as lines that had variables related to it. That way, I was able to figure out how
to fix numerous errors. However, not all bugs interfered with the running process. But by repeatedly 
running the game and playing it, I was able to identify quite a few of them myself. Then I would look 
into the code related to the issue and use breakpoints to debug it.

### Testing

Since I found most of the bugs using the debugger, I didn't use the tests as much as I expected to.
One of the last bugs I fixed was in the test file itself. However, without tests I would have never 
found one last error that would have been impossible to identify just by running the code- the initial
card deck having 56 cards instead of 52. So although I found most errors without using tests, it 
really helped me identify the bug I wouldn't have found otherwise.

## Extending code base

To extend the code base, I have done quite a few things that can be generalised into 3 categories:

### 1. Player changes
Changes affecting the human player include additional choices. Now the player is able to choose 
voluntarily not to discard any cards during their turn. In addition, when a card is drawn after no
discards were made (either no discards available or the player chose not to discard any cards),
the player can choose whether they want to discard it or add it to their hand.

### 2. AI changes
This is where most code extension was implemented. Firstly, I added some AI name choices to increase variety. 
Then, with addition of player choices, I made them apply to AIs as well. AIs can now choose
voluntarily not to discard any cards (SmartAI already had this option but SimpleAI didn't). Additionally, 
when a card is drawn after no discards were made, AIs can choose not to discard it. SimpleAIs do it randomly, 
however, I implemented a strategy for SmartAIs not to discard when it can be beneficial for them.

### 3. UI changes
Additionally, I have made some changes to the UI. New information displayed every round is the current player's 
index (instead of number of hands), current player's hand size, game direction (1 is clockwise, -1 is anticlockwise), 
and the rest is unchanged. Furthermore, I added messages differentiating whether the player could not discard 
a card or voluntarily chose not to do so, as well as showing whether the player chose to add a drawn card to hand if 
it could have been discarded. 