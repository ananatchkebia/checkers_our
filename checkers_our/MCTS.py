import random
import math
import copy
BLUE = (0, 0, 255)
RED = (255, 0 , 0)


class TreeNode():
    #class constructor (create tree node class instance)
    def __init__(self, board, parent):
        #init associated board state
        self.board = copy.deepcopy(board)
        #init is node terminal (flag)
        if self.board.is_win() :
            #we have a terminal node
            self.is_terminal = True
        else:
            #we have a non-terminal node
            self.is_terminal = False
        
        #set is fully expanded flag
        self.is_fully_expanded = self.is_terminal   
        self.parent = parent
        
        #init the number of node visits
        self.visits = 0
        
        #init the total score of the node
        self.score = 0
        
        #init current node's children
        self.children = {}
        
class MCTS():
    #search for the best move in the current position
    def search(self, initial_state):
        #create root node
        #print(initial_state)
        #print("here is the beginning of search")
        self.root = TreeNode(initial_state, None)
        #walk through 1000 iterations
        for iteration in range(10):
            print("player:",self.root.board.player)
            #print("here is search iteration")
            #select a node (selection phase)
            node = self.select(self.root)
            #print(node.board.board_representation())
            if(node.board.player == BLUE): node.board.player = RED
            else: node.board.player = BLUE
            #score current node (simulation phase)
            score = self.rollout(node.board)
            # backpropagate results            
            self.backpropagate(node, score)
        #pick up the best move in the current position    
        try:
            #print("the last state:")
            #self.get_best_move(self.root, 0).board.board_representation()
            return self.get_best_move(self.root, 0)
        except:
            pass
        
    # select most promising node
    def select(self, node):
        #print("here is the beginning of select")
        #make sure that we're dealing with non-terminal nodes
        while not node.is_terminal:
            #print("here is select loop")
            # case where the node is fully expanded
            if node.is_fully_expanded:
                node = self.get_best_move(node, 2)
                if(node.board.player == BLUE): node.board.player = RED
                else: node.board.player = BLUE
                #print("this is get_best_move result:")
                #print(node.board.board_representation())
                #print()
                #print()
            # case where the node is not fully expanded
            else:
                #otherwise expand the node
                return self.expand(node)
        return node
    
    #expand node
    def expand(self, node):
        #print("here is the beginning of expand")
        # generate legal states (moves) for the given node
        states = node.board.generate_states(node.board.player)
        # loop over generated states (moves)
        #print(node.children)
        for state in states:
            #make sure that current state (move) is not present in child nodes
            if state.string_repr() not in node.children:
                #create a new node
                new_node = TreeNode(state, node)
                
                #add child node to parent's node children list (dict)
                node.children[state.string_repr()] = new_node
                
                #case where node is fully expanded or not
                if len(states) == len(node.children):
                    node.is_fully_expanded = True


                #return newly created node
                return new_node   
            
        #debugging
        print('Should not get here!!!')    
    # simulate the game via making random moves until reach end of the game
        
    def rollout(self, board):
        #print("here is the beginning of rollout")
        # make random moves for both sides until terminal state of the game is reached
        while not board.is_win():
            #print("here is rollout loop")
            #try to make a move
            try:
                #make the on board
                #print(board.player_1)
                
                board = random.choice(board.generate_states(board.player))
                if(board.player == BLUE):board.player = RED
                else:board.player = BLUE
                #board.board_representation()
                #no moves available
            except:
                #return a draw score
                return 0
        #return score from the player "BLUE" perspective
        if board.player == BLUE:return 1
        elif board.player == RED: return -1


    # backpropogate the number of visits and score up to the root node
    def backpropagate(self, node, score):
        # update nodes' up to root node
        while node is not None:
            #update nodes' visits
            node.visits += 1
            #update nodes' score
            node.score += score
            # set node to parent
            node = node.parent
    
    # select the best node basing on UCB1 formula
    def get_best_move(self, node, exploration_constant):
        #define best score & best moves
        best_score = float('-inf')
        best_moves = []
        
        #loop over child nodes
        for child_node in node.children.values():
            #define current player
            if child_node.board.player == BLUE : current_player = 1
            elif child_node.board.player == RED : current_player = -1
            
            # get move score using UCT formula
            move_score = current_player * child_node.score / child_node.visits + exploration_constant * math.sqrt(math.log(node.visits / child_node.visits))
            #better move has been found
            if move_score > best_score:
                best_score = move_score
                best_moves = [child_node]
            #found as good move as already available
            elif move_score == best_score:
                best_moves.append(child_node)
            #return one of the best moves randomly
  
        return random.choice(best_moves) 
