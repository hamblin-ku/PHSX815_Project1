import numpy as np
import argparse
from Random import Random
    
# main function for this Python code
if __name__ == "__main__":
    
    # Set up parser to handle command line arguments
    # Run as 'python monopoly_sim.py -h' to see all available commands
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", "-s", help="Seed number to use")
    parser.add_argument("--Nsides",  help="Number of sides on each die")
    parser.add_argument("--Ngames",  help="Number of games to simulate ")
    parser.add_argument("--Nturns",  help="Number of turns to roll for")
    args = parser.parse_args()

    # default seed
    seed = 5555
    if args.seed:
        print("Set seed to %s" % args.seed)
        seed = args.seed
    
    # By default, roll 6 sided dice
    Nsides = 6
    if args.Nsides:
        print("Number sides per die: %s" % args.Nsides)
        Nsides = args.Nsides
    
    Nturns = 50
    if args.Nturns:
        print("Number of turns: %s" % args.Nturns)
        Nturns = args.Nturns
        
    Ngames = 100
    if args.Ngames:
        print("Number of games: %s" % args.Ngames)
        Ngames = args.games
    
    # List of properties
    properties = ["Go", "Mediterranean Avenue", "Community Chest", "Baltic Avenue", "Income Tax", "Reading Railroad", "Oriental Avenue", "Chance", "Vermont Avenue", "Connecticut Avenue", "Jail", "St. Charles Place", "Electric Company", "States Avenue", "Virginia Avenue", "Pennsylvania Railroad", "St. James Place", "Community Chest", "Tennessee Avenue", "New York Avenue", "Free Parking", "Kentucky Avenue", "Chance", "Indiana Avenue", "Illinois Avenue", "B&O Railroad", "Atlantic Avenue", "Ventnor Avenue", "Water Works", "Marvin Gardens", "Go To Jail", "Pacific Avenue", "North Carolina Avenue", "Community Chest", "Pennsylvania Avenue", "Short Line", "Chance", "Park Place", "Luxury Tax", "Boardwalk"]
    
    # For future use
    # jail corresponds to the 10th tile, 'Go to Jail' is the 30th tile
    pos_jail, pos_goToJail = 10, 30
    
    # 'Chance' and 'Community Chest' tiles:
    #   To simulate the drawing of a card from these tiles, we will randomly generate an integer from 1 to 16. If the number matches the
    #   index of a card that sends the player to go/jail, the action will be performed. Then, and if the number did not match such an index,
    #   the drawn card will be removed from the pile, and the value stored in a separate array tracking drawn cards. Eventually, if the pile
    #   is emptied, all cards will be placed back in the deck. If the index of a card that is in the drawn pile is drawn, another random number
    #   will be returned until a new one is drawn
    
    # EDIT:
    # I will refine the method of drawing cards, since right now it could conceivably take a long time to get a card if the pile is almost empty.
    # I will probably physically shrink the size of the card pile as a card is taken out, and then only draw numbers from 1 to new size of the array,
    # so that the return number is always valid and a new number does not have to be drawn. It will be much quicker.
    # Also, I will create functions above main to perform these chance/chest operations, as they will consist of variety of conditional statements and may be long.
    # These functions will return the position that the player moves to (if they don't move, it returns the current position). 
    
    # Positions of 'Chance' tiles
    #   There are 16 total cards, but only 10 cards of interest. The following are where these cards of interest send the player if they are drawn:
    #   Card Index in Deck:
    #   (0)     'GO' [0]
    #   (1)     jail [10]
    #   (2)     Boardwalk [39]
    #   (3)     St. Charles Place [11]
    #   (4)     Nearest utility tile [12 or 28]
    #   (5)     Illinois Avenue [24], Reading Railroad [5]
    #   (6)     Go back 3 spaces
    #   (7)     Nearest Railroad  [15, 25, or 5]
    #   (8)     Nearest Railroad  [15, 25, or 5]
    pos_chance = np.array([7, 22, 36])
    
    # Positions of 'Community Chest' tiles
    #   There are 16 cards total, and two cards in this pile of note. The following are where these cards of interest send the player if they are drawn:
    #   Card Index in Deck:
    #   (1)     'GO' [0]
    #   (2)     jail [10]
    #
    #   Note that the arbitary definitions of these positions does not matter, due to the random nature of how the cards are to be drawn.
    pos_chest = np.array([2, 17, 33])
    
    # Initialize arrays for keeping track of drawn cards.
    chance_drawn = []
    chest_drawn = []
    
    # Array to totalthe frequency of player position per tile as a function of turns. Nturns x 40 matrix
    # where each row corresponds to a subsequent turn
    #
    # This way, the data can be analyzed by plotting the probability (normalized frequency) of being at any one tile for any turn
    # To help visualzie this:
    #
    #       (turn #)        (tile 0)    (tile 1)    (tile 2)    ...     (tile 39)
    #           1             ---         ---         ---       ...        ---
    #           2             ---         ---         ---       ...        ---
    #           3             ---         ---         ---       ...        ---
    #           .              .           .           .                    .
    #           .              .           .           .                    .
    #           .              .           .           .                    .
    #         Nturn           ---         ---         ---       ...        ---
    #
    obs = np.zeros( shape= (Nturns, 40)  )
    
    
    ## NOTE
    # need to differentiate between passing through jail and being in jail
    # maybe keep separate array for tracking being in jail per turn -> 41 total tiles ?
    
    # Class instance of our Random class using seed
    # Will use the Random.int(N) method to get random integer from 1 to N
    # This will simulate the die roll for an N sided die
    # For k N sided dice, Random.int(N) will be called k times
    random = Random(seed)
    
    
    # Iterate through each game to simulate, where each 'game' consists of Nturns number of turns
    for i in range(Ngames):
        #Initialize current position to be at 'GO' [0]
        cpos = 0
        for j in range(Nturns):
            # Counter to keep track of doubles
            double_count = 0
            
            die_1 = random.int(Nsides)
            die_2 = random.int(Nsides)
            
            #If third double, send to jail
            if die_1 == die_2 and doube_count == 2:
                cpos = 10
                # code to add 1 to jail tally for turn j
            
            cpos += (die_1 + die_2)
            
            # code here to check for chance/chest tile
            
            #Now check for doubles
            if die_1 == die_2:
                #Roll again
                die_1 = random.int(Nsides)
                die_2 = random.int(Nsides)
                
                #perform same checks as above; might make sense to put all this in functiona n d recursively call it
                # inputs could be the current number of doubles rolled and the current position?
                #  pos_end = turn(cpos, N_currDouble)
                #
                #   def turn(start_pos, N_curr_Double):
                #       if N_curr_Double == 3:
                #           return pos_jail
                #       roll dice code/update position
                #       check if chance/chest, draw and call funcs
                #
                #       now check if doubles rolled again
                #       if yes:
                #           new_pos = turn(new_pos, N_curr_Double + 1)
                #       return new_pos
                #
                #   I think the above would work, need to play with it for a bit; it would shorten the code a lot 
                
            
    
