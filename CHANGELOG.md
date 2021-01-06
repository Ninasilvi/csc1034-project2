# CHANGELOG 
* v1.1.6 [2021-01-06]: Changed `self.players[1]` to `self.players[i]` in `switch.py` line 79.  
    UI now displays the correct winner.
* v1.1.5 [2021-01-06]: 
    * Changed `self.direction == 1` to `self.direction = 1` in `switch.py` line 97.
    * Changed `return False` to `return True` in `switch.py` line 159.  
    Q and A cards are now discardable.
* v1.1.4 [2021-01-06]: 
    * Changed `player, idx` to `idx, player` in `user_interface.py` line 127.
    * Changed `players.name` to `player.name` and `players.hand` to `player.hand` in `user_interface.py` line 128.  
    Now possible to swap hands for J card effect.
* v1.1.3 [2021-01-05]: Changed `self.players = [player_classes[typ](name) for typ, name in player_info]` to 
`self.players = [player_classes[typ](name) for typ, name in player_info]` in  `switch.py` line 52.  
    The game starts.
* v1.1.2 [2021-01-04]: Changed `player_classes(name)` to `player_classes[name]` in `switch.py` line 52.
* v1.1.2 [2021-01-03]: Changed `Switch().run_game` in `switch.py` to `game = Switch()`
  `game.run_game()`.  
    The UI starts when running `switch.py`.

* v1.1.1 [2021-01-03]: 
  * Changed player to players in `user_interface.py` line 128.
  * Changed card to i in `user_interface.py` line 113.
  * Added missing indentation in `switch.py` line 198.

* v1.1.1 [2020-12-23]: Fixed open bracket in `players.py` line 50.

* v1.1.0 [2019-11-08]: Added a SmartAI computer opponent.
  Added strategy players.SmartAI.
  None of the bugs have been fixed.

* v1.1.0 [2019-10-25]: First major release.
  This version is known to contain some bugs.
  

