# PHSX815 Project 1
## Monopoly Simulation
### Description:
For this project, I will simulate a game of monopoly (from the persepcive of one player). I generate random dice rolls using the methods developed in class (see random.int(N) in Random.py), and will keep track of the end positions of the player after every turn, following the traditional rules of the game (including 'Chance' and 'Community Chest' cards.

### Parameters:
The user is able to specify the numbers of sides on the dice being used. ZThe default is 6, but any value > 0 can be used. I may also add functionality to use biased dice, as this would be trivial.

### Experiment Outputs
A plot of the probability of landing on any tile for a given turn. I will make such plots for simulations using different sided dice, perhaps with a d6, d12, and d20. It will be interesting to compare the overall patterns. I think I will also do so using two biased 6 sided dice, and perhaps the analysis can include trying to distinguish between the results of biased/un-biased dice (hyothesis testing). 

### Changes:
####Jail:
It is assumed that the player will get out of jail as soon as possible (by paying the $50 fine on the next turn), as opposed to waiting in jail until they get out automatically. This is a fair assumption since most players would make this choice early in the game, which is primarily where this project will be looking at.

