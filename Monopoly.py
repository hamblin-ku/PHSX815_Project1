# File:     Monopoly.py
# Author:   Kurt Hamblin
# Description:  Monopoly() class that can simulate a game of Monopoly. Generalized format to allow future expansion.

from Random import Random
import numpy as np


class Monopoly:
    """A Monopoly game class"""
    
    ##################
    # INITIALIZE ONCE
    ##################
    
    # Positions of various tiles
    pos_jail = 10
    pos_goToJail = 30
    pos_chance = np.array([7, 22, 36])
    pos_chest = np.array([2, 17, 33])
    
    # Tile Names
    properties = ["Go", "Mediterranean Avenue", "Community Chest", "Baltic Avenue", "Income Tax", "Reading Railroad", "Oriental Avenue", "Chance", "Vermont Avenue", "Connecticut Avenue", "Just Visiting/Jail", "St. Charles Place", "Electric Company", "States Avenue", "Virginia Avenue", "Pennsylvania Railroad", "St. James Place", "Community Chest", "Tennessee Avenue", "New York Avenue", "Free Parking", "Kentucky Avenue", "Chance", "Indiana Avenue", "Illinois Avenue", "B&O Railroad", "Atlantic Avenue", "Ventnor Avenue", "Water Works", "Marvin Gardens", "Go To Jail", "Pacific Avenue", "North Carolina Avenue", "Community Chest", "Pennsylvania Avenue", "Short Line", "Chance", "Park Place", "Luxury Tax", "Boardwalk"]
    

    # initialization method for Monopoly class
    def __init__(self, seed = 5555, Nsides = 6, weights= None):
        self.Nsides = Nsides
        self.weights = weights
        self.random = Random(seed)
    
        # Positions of 'Chance' tiles
        #   There are 16 total cards, but only 10 cards of interest. The following are where these cards of interest send the player if they are drawn:
        #   Card Index in Deck:
        #   (0)     'GO' [0]
        #   (1)     jail [40]
        #   (2)     Boardwalk [39]
        #   (3)     St. Charles Place [11]
        #   (4)     Nearest utility tile [12 or 28]
        #   (5)     Illinois Avenue [24],
        #   (6)     Reading Railroad [5]
        #   (7)     Go back 3 spaces
        #   (8)     Nearest Railroad  [15, 25, or 5]
        #   (9)     Nearest Railroad  [15, 25, or 5]
        self.deck_chance = [0, Monopoly.pos_jail, 39, 11, 'NU', 24, 5, 'B3', 'NR', 'NR', None, None, None, None, None, None]
        self.numInChance = 16
        
        # Positions of 'Community Chest' tiles
        #   There are 16 cards total, and two cards in this pile of note. The following are where these cards of interest send the player if they are drawn:
        #   Card Index in Deck:
        #   (1)     'GO' [0]
        #   (2)     jail [40]
        #
        #   Note that the arbitary definitions of these positions does not matter, due to the random nature of how the cards are to be drawn.
        self.deck_chest = [0, Monopoly.pos_jail, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        self.numInChest = 16
        
    # Separate methods for shuffling in case implementation changes in the future
    def shuffle_chance(self):
        """Shuffle Chance Deck"""
        self.deck_chance = [0, Monopoly.pos_jail, 39, 11, 'NU', 24, 5, 'B3', 'NR', 'NR', None, None, None, None, None, None]
        self.numInChance = 16

    def shuffle_chest(self):
        """Shuffle Community Chest Deck"""
        self.deck_chest = [0, Monopoly.pos_jail, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        self.numInChest = 16
    
    def _draw_chest(self, start_pos):
        """Draw a card from Community Chest deck"""
        #If chest deck is empty, re-initialize it
        if self.numInChest == 0:
            self.shuffle_chest()
            
        # Use Random Class to randomly draw a card
        # We generate an index of card to draw, in order to take into account the shrinking of the deck. Ranges from 0 to current deck size - 1
        cardIndexToDraw = self.random.roll_die(Nsides = self.numInChest) - 1
        
        #Subtract one card from deck length
        self.numInChest -= 1
        
        drawnCard = self.deck_chest[cardIndexToDraw]
        self.deck_chest = np.delete(self.deck_chest, cardIndexToDraw)
        
        # If the drawn card has no action, the player doesn't move.
        if drawnCard == None:
            return start_pos
        # Otherwise, return the position the card moves the player to
        else:
            return drawnCard

    def _draw_chance(self, start_pos):
        """Draw a card from Chance deck"""
        #If chance deck is empty, re-initialize it
        if self.numInChance == 0:
            self.shuffle_chance()
            
        # Use Random Class to randomly draw a card
        # We generate an index of card to draw, in order to take into account the shrinking of the deck. Ranges from 0 to current deck size - 1
        cardIndexToDraw = self.random.roll_die(Nsides = self.numInChance) - 1
        
        #Subtract one card from deck length
        self.numInChance -= 1
        
        drawnCard = self.deck_chance[cardIndexToDraw]
        deck_chance = np.delete(self.deck_chance, cardIndexToDraw)
        # If the drawn card has no action, the player doesn't move.
        if drawnCard == None:
            return start_pos
        # Otherwise, return the position the card moves the player to
        elif drawnCard == 'NU':
            #find which utility is closest
            if abs(12 - start_pos) < abs(28 - start_pos):
                return 12
            else:
                return 28
        elif drawnCard == 'B3':
            return start_pos - 3
        elif drawnCard == 'NR':
            if abs(15 - start_pos) < abs(25 - start_pos) and abs(15 - start_pos) < abs(5 - start_pos):
                return 15
            elif abs(25 - start_pos) < abs(5 - start_pos):
                return 25
            else:
                return 5
        else:
            return drawnCard

    def reset(self):
        """Reset the board"""
        self.shuffle_chance()
        self.shuffle_chest()

    def _turn(self, start_pos, N_curr_Double):
        """Perform a turn and return new player position"""
        
        # If this is the third double in a row, immediately send player to Jail
        if N_curr_Double == 3:
            return Monopoly.pos_jail
        
        # Roll the dice
        die_1 = self.random.roll_die(Nsides=self.Nsides, weights = self.weights)
        die_2 = self.random.roll_die(Nsides=self.Nsides, weights = self.weights)
        new_pos = start_pos + die_1 + die_2
        
        # Check to see if player landed on 'go to jail'. If yes, end turn
        if new_pos == Monopoly.pos_goToJail:
            return Monopoly.pos_jail
        # Now check to see if player has wrapped around board
        elif new_pos >= 40:
            new_pos = new_pos % 40
        
        # Check to see if player landed on a 'Chance' or 'Community Chest' tile
        if new_pos in Monopoly.pos_chance:
            new_pos = self._draw_chance(new_pos)
        elif new_pos in Monopoly.pos_chest:
            new_pos = self._draw_chest(new_pos)
                
        # Now check to see if player rolled doubles
        if die_1 == die_2:
            # Recursive call of turn() to handle rolling doubles
            new_pos = self._turn(new_pos, N_curr_Double + 1)
        return new_pos
    
    def play_games(self, Nturns=50, Ngames = 1, norm = False):
        """ Simulate Monopoly games.
            
            Keyword Arguments:
            Nturns -- the number of turns per game (default 50)
            Ngames -- the number of games (default 1)
            norm -- normalize or not (defalt False)
        """
        # Construct array for tracking player positions for each turn
        positions = np.zeros( shape = (Nturns, 40)  )
        
        # Factor to normalize by. If norm == False, factor is simply 1
        factor = 1
        if norm:
            factor /= Ngames
        
        # iterate through each game
        for game in range(Ngames):
            # Start player at 'GO'
            player_pos = 0
            
            # Iterate through each turn
            for turn in range(Nturns):
                # Update the player position
                player_pos = self._turn(start_pos = player_pos, N_curr_Double = 0)
                
                # Record where the player landed
                positions[turn][player_pos] += factor
                
            # Reset the board
            self.reset()
        return positions
