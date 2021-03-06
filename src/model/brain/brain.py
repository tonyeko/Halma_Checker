from abc import ABCMeta
from time import time
from random import choice

class Brain(metaclass=ABCMeta):
    '''Base class of brain for the AI implemented in Halma Game
    '''
    
    def __init__(self):
        self.computing_time = None
        self.total_computing_time = 0
        
    def update_total_computing_time(self):
        """Update total computing time of this brain
        """
        self.total_computing_time += self.computing_time
    
    def reset(self):
        """Reset attributes
        """
        self.thinking_time = time() + self.t_limit
    
    def inject(self, t_limit):
        """Inject t_limit to brain
        """
        self.t_limit = t_limit
        
    def terminate(self, depth, state):
        """Terminate brain

        Args:
            depth (int): depth of tree
            state (State): current state

        Returns:
            boolean: True if terminate condition
        """ 
        p1_win, p2_win = state.win_condition()
        return depth == self.max_depth or p1_win or p2_win or time() > self.thinking_time
    
    def find_best_move(self, state, max_depth = 3):
        '''Find best move with minimax + local search
        
        Parameters:
            state (State): Current Game State
        
        Returns:
            State: Next state with best move being done by AI 
        '''
        self.reset()
        self.max_depth = max_depth
        self.which_player = state.currentPlayer
        start_time = time()
        best_moves, _ = self.minimax(state, state.currentPlayer == state.player_2)
        self.computing_time = time() - start_time
        self.update_total_computing_time()
        if best_moves == None:
            possible_moves = state.current_player_possible_moves()
            move = choice(list(possible_moves))
            move_to_random = choice(list(move['to']))
            return (move['from'], move_to_random)
        return best_moves
