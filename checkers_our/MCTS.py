import random
import math
BLUE = (0, 0, 255)
RED = (255, 0 , 0)
'''
class TreeNode():
    #class constructor (create tree node class instance)
    def __init__(self, board, parent):
        #init associated board state
        self.board = board
        
        #init is node terminal (flag)
        if self.board.is_win():
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
        print("I am in search")
        self.root = TreeNode(initial_state, None)
        print(self.root.board.board_representation())
        #walk through 1000 iterations
        for iteration in range(10):
            print("I am in loop ",iteration)
            #select a node (selection phase)
            node = self.select(self.root)
            #score current node (simulation phase)
            score = self.rollout(node.board)
            # backpropagate results
            self.backpropagate(node, score)
        #pick up the best move in the current position    
        try:
            return self.get_best_move(self.root, 0)
        except:
            pass
    # select most promising node
    def select(self, node):
        print("I am in select")
        #make sure that we're dealing with non-terminal nodes
        while not node.is_terminal:
            print("I am in while loop")
            # case where the node is fully expanded
            if node.is_fully_expanded:
                node = self.get_best_move(node, 2)
                
            # case where the node is not fully expanded
            else:
                #otherwise expand the node
                return self.expand(node)

        return node
    
    #expand node
    def expand(self, node):
        print("I am in expand")
        # generate legal states (moves) for the given node
        states = node.board.generate_states()
        #for state in states:
        #    state.board_representation()

        # loop over generated states (moves)
        for state in states:
            #make sure that current state (move) is not present in child nodes
            #print("here: ",str(state))
            #print(node.children)
            
            if state not in node.children:
                
                #create a new node
                new_node = TreeNode(state.board, node)
                
                #add child node to parent's node children list (dict)
                node.children[state] = new_node
                
                #case where node is fully expanded or not
                if len(states) == len(node.children):
                    node.is_fully_expanded = True

                #return newly created node
                return new_node   
            
        #debugging
        print('Should not get here!!!')    
    # simulate the game via making random moves until reach end of the game
    def rollout(self, board):
        # make random moves for both sides until terminal state of the game is reached
        while not board.is_win():
            print("I am in rollout while loop")
            #try to make a move
            try:
                #make the on board
                board = random.choice(board.generate_states())
                #no moves available
            except:
                #return a draw score
                return 0
        #return score from the player "x" perspective
        if board.player_2 == BLUE:return 1
        elif board.player_2 == RED: return -1

    # backpropogate the number of visits and score up to the root node
    def backpropagate(self, node, score):
        # update nodes' up to root node
        while node is not None:
            print("I am in backpropagate while loop")
            #update nodes' visits
            node.visits += 1
            #update nodes' score
            node.score += score
            # set node to parent
            node = node.parent

    # select the best node basing on UCB1 formula
    def get_best_move(self, node, exploration_constant):
        print("I am in get_best_move method")
        #define best score & best moves
        best_score = float('-inf')
        best_moves = []
        
        #loop over child nodes
        for child_node in node.children.values():
            #define current player
            if child_node.board.player_2 == BLUE : current_player = 1
            elif child_node.board.player_2 == RED : current_player = -1
            
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
'''    

class TreeNode():
    #class constructor (create tree node class instance)
    def __init__(self, board, parent):
        #init associated board state
        self.board = board
        
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
        self.root = TreeNode(initial_state, None)
        #walk through 1000 iterations
        for iteration in range(10):
            #select a node (selection phase)
            node = self.select(self.root)
            #score current node (simulation phase)
            score = self.rollout(node.board)
            # backpropagate results
            self.backpropagate(node, score)
        #pick up the best move in the current position    
        try:
            return self.get_best_move(self.root, 0)
        except:
            pass
    # select most promising node
    def select(self, node):
        #make sure that we're dealing with non-terminal nodes
        while not node.is_terminal:
            # case where the node is fully expanded
            if node.is_fully_expanded:
                node = self.get_best_move(node, 2)
                
            # case where the node is not fully expanded
            else:
                #otherwise expand the node
                return self.expand(node)

        return node
    
    #expand node
    def expand(self, node):
        # generate legal states (moves) for the given node
        states = node.board.generate_states()
        # loop over generated states (moves)
        
        for state in states:
            #make sure that current state (move) is not present in child nodes
            if str(state.board) not in node.children:
                #create a new node
                new_node = TreeNode(state, node)
                
                #add child node to parent's node children list (dict)
                node.children[str(state.board)] = new_node
                
                #case where node is fully expanded or not
                if len(states) == len(node.children):
                    node.is_fully_expanded = True

                #return newly created node
                return new_node   
            
        #debugging
        print('Should not get here!!!')    
    # simulate the game via making random moves until reach end of the game
    def rollout(self, board):
        # make random moves for both sides until terminal state of the game is reached
        while not board.is_win():
            #try to make a move
            try:
                #make the on board
                board = random.choice(board.generate_states())
                #no moves available
            except:
                #return a draw score
                return 0
        #return score from the player "x" perspective
        if board.player_2 == BLUE:return 1
        elif board.player_2 == RED: return -1

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
            if child_node.board.player_2 == BLUE : current_player = 1
            elif child_node.board.player_2 == RED : current_player = -1
            
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



