# COMP 4190: A3 - Reinforcement Learning
# Instructor: Dr. Cuneyt G Akcora
# Student Names and Numbers:
# Aaron Salo - 7805174
# Nicholas Duan - 7742401

import enum as Enum
from re import X

class State(object):

    symbol = '_'
    def __init__(self, cost):
        self.actions = ['N', 'S', 'E', 'W']
        self.cost = cost

        self.utility = 0

        #value iteration
        self.optimalValue = 0.0
        self.policy = 'N'

        #qvalue learning
        self.qvalues = {
            "N":0.0,
            "E":0.0,
            "S":0.0,
            "W":0.0,
        }

    
    #toString function
    def __str__(self):
         return self.symbol
    
    #another toString function (idk its some python stuff)
    def __repr__(self):
        return self.symbol


class Terminal(State):
    symbol = 'T'

    def __init__(self, cost):
        super().__init__(cost)
        self.actions = ['EXIT'] 
        
        self.qvalues = {
            "EXIT":0.0
        }



class Boulder(State):
    symbol = 'B'
    
    def __init__(self):
        super().__init__(0)
        self.actions = []    

