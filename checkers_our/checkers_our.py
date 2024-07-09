from pickle import NONE
import pygame
import copy
import random
import time
from MCTS import * 


WIDTH, HEIGHT = 500, 500
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS 


RED = (255, 0 , 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY =  (128, 128, 128)
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44,25))


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


FPS = 60


#Following is auxiliary method to detect on which square does mouse clicked
def get_row_col_with_mouse_pos(pos):
    x,y = pos
    row = y//SQUARE_SIZE 
    col = x//SQUARE_SIZE 
    return row, col




class Piece:
    PADDING = 10
    OUTLINE = 2
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.killer = False
        self.calc_pos()
        
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
        
    def make_king(self):
       self.king = True
       
    def draw(self,win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win,GREY,(self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win,self.color,(self.x, self.y), radius )
        if(self.king):
            win.blit(CROWN,(self.x - CROWN.get_width()//2,self.y - CROWN.get_height()//2))
            
    
class Square:
    def __init__(self, sq_color,piece = None ):
        self.square_color = sq_color
        self.piece = piece
        
class Board:
    def __init__(self, win =None):
        self.board = []
        
        self.player = RED
        
        for i in range(ROWS):
            self.board.append([])
            for j in range(COLS):
                if (not (i % 2)) and (not(j % 2)) :
                    self.board[i].append(Square(BLACK)) 
                    pygame.draw.rect(win, BLACK, (i * SQUARE_SIZE,j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif (not(i % 2)) and (j % 2) :
                    self.board[i].append(Square(WHITE))
                    pygame.draw.rect(win, WHITE, (i * SQUARE_SIZE,j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif (i % 2) and (not(j % 2)) :
                    self.board[i].append(Square(WHITE))
                    pygame.draw.rect(win, WHITE, (i * SQUARE_SIZE,j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif (i % 2) and (j % 2) :
                    self.board[i].append(Square(BLACK)) 
                    pygame.draw.rect(win, BLACK, (i * SQUARE_SIZE,j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


        self.initial_setup(win)
        
    def initial_setup(self,win):
        for i in range(0,3):
            for j in range(COLS):
                if self.board[i][j].square_color == BLACK:
                    self.board[i][j].piece = Piece(i,j,BLUE)
                    self.board[i][j].piece.draw(win)
        for i in range(5,8):
            for j in range(COLS):
                if self.board[i][j].square_color == BLACK:
                    self.board[i][j].piece = Piece(i,j,RED)
                    self.board[i][j].piece.draw(win)
                    
    #get square which are legal to move current piece 
    def valid_squares_to_move(self,row,col):
        valid_squares_row_col_dict = {}
        if(self.board[row][col].piece.color == RED):
            if(col != 7 and row <= 7):
                if(self.board[row - 1][col + 1].piece == None):
                    if(row - 1 >= 0 and col + 1 < 8):
                        valid_squares_row_col_dict["UpRight"]=[row - 1, col + 1]
                elif(col != 6):
                    if(self.board[row - 1][col + 1].piece.color == BLUE and self.board[row - 2][col + 2].piece == None):
                        if(row - 2 >= 0 and col + 2 < 8):
                            valid_squares_row_col_dict["UpRightKill"]=[row - 2, col + 2]
            if(self.board[row - 1][col - 1].piece == None):
                if(row - 1 >= 0 and col - 1 >= 0 ):
                    valid_squares_row_col_dict["UpLeft"]=[row - 1, col - 1]
            elif(self.board[row - 1][col - 1].piece.color == BLUE and self.board[row - 2][col - 2].piece == None):
                if(row - 2 >= 0 and col - 2 >= 0 ):
                    valid_squares_row_col_dict["UpLeftKill"]=[row - 2, col - 2]
                   
        if(self.board[row][col].piece.color == BLUE):
            if(col != 7 and row <7):
                if(self.board[row + 1][col + 1].piece == None):
                    if(row + 1 <= 8 and col + 1 < 8):
                        valid_squares_row_col_dict["DownRight"]=[row + 1, col + 1]
                elif(col != 6 and row < 6):
                        if(self.board[row + 1][col + 1].piece.color == RED and self.board[row + 2][col + 2].piece == None):
                            if(row + 2 < 8 and col + 2 < 8):
                                valid_squares_row_col_dict["DownRightKill"]=[row + 2, col + 2]
            if(row <7):
                if(self.board[row + 1][col - 1].piece == None):
                    if(row + 1 <= 8 and col - 1 >= 0):
                        valid_squares_row_col_dict["DownLeft"]=[row + 1, col - 1]
                elif(row <6):
                    if(self.board[row + 1][col - 1].piece.color == RED and self.board[row + 2][col - 2].piece == None):
                        if(row + 2 < 8 and col - 2 >= 0 ):
                            valid_squares_row_col_dict["DownLeftKill"]=[row + 2, col - 2]
        
        return valid_squares_row_col_dict
    
    def board_representation(self):
        for row in range(ROWS):
            for col in range(COLS):
                if(self.board[row][col].piece is not None):
                    print(self.board[row][col].piece.color,"     ",end='')
                else:
                    print("emptySquare","     ",end='')
            print()            
    def make_move(self,y1,x1,y2,x2,win = False,valid = False):
        #If movement is legal than make move
        if self.is_legal_move(y1,x1,y2,x2) or valid:
           #Check if this movement is simple movement or killing opponent's piece
           #In any case we have to do one action similarly,and this action is after following if condition
           #But in case of killing, we have to do one additional action
           #We have to take opponent's piece from the board 
            if(abs(y2-y1) == 2):
                
                self.board[y1][x1].piece.killer = True
                  #detect location of opponent's piece
                if(y2>y1 and x2>x1):
                    self.board[y1+1][x1+1].square_color = BLACK
                    self.board[y1+1][x1+1].piece = None
                    if(win != False):
                        pygame.draw.rect(win, BLACK, ((x1+1) * SQUARE_SIZE,(y1+1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif(y2>y1 and x2<x1):
                    self.board[y1+1][x1-1].square_color = BLACK
                    self.board[y1+1][x1-1].piece = None
                    if(win != False):
                        pygame.draw.rect(win, BLACK, ((x1-1) * SQUARE_SIZE,(y1+1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif(y2<y1 and x2<x1):
                    self.board[y1-1][x1-1].square_color = BLACK
                    self.board[y1-1][x1-1].piece = None
                    if(win != False):
                        pygame.draw.rect(win, BLACK, ((x1-1) * SQUARE_SIZE,(y1-1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif(y2<y1 and x2>x1):
                    self.board[y1-1][x1+1].square_color = BLACK
                    self.board[y1-1][x1+1].piece = None
                    if(win != False):
                        pygame.draw.rect(win, BLACK, ((x1+1) * SQUARE_SIZE,(y1-1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


            #this is simple movement,so we just have to swap values on the board's following locations[y1][x1] and [y2][y1] 
            self.board[y2][x2], self.board[y1][x1] = self.board[y1][x1], self.board[y2][x2]
            if(win != False):
                pygame.draw.rect(win, BLACK, (x1 * SQUARE_SIZE,y1 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if(self.board[y2][x2].piece.color == BLUE):
                if(win != False):
                    Piece(y2,x2,BLUE).draw(win)
            if(self.board[y2][x2].piece.color == RED):
                if(win != False):
                    Piece(y2,x2,RED).draw(win)
    def is_legal_move(self,y1,x1,y2,x2):
        for valid_square in self.valid_squares_to_move(y1,x1).values():
            if(valid_square[0] == y2 and valid_square[1] == x2):return True
        return False
    
    
    def sequential_kills_possible(self,color):
        possible_sequential_kills = []
        if self.kill_is_possible(color) != False:
                
            '''
            #we must iterate on killing_positions and create copy of new board with these kills and check if in potential
            #board still is possible make kill with the same piece
            #but now we must take in mind the fact that after first killing valid moves will change
            #piece can kill in backward as well as forward
            #I want to have list of lists,each inner list should be sequence of positions from start position(where killer piece 
            #stands at the begining of killing) to end position(where killer piece will stand after performing all kills)
            #and number of inner lists should be equal to number of all possible different ways how player can perform killing movement
            #One way is one movement,which player can do
            #this following counter counts number of inner lists,so number of possible movements
            '''
            
            counter = 0
            for kill_position in self.kill_is_possible(color)[1]:
                valid_moves = self.valid_squares_to_move(kill_position[0],kill_position[1])
                valid_moves = {key : value for key, value in valid_moves.items() if "Kill" in key}                
                temp_board = copy.deepcopy(self)
                
                for move in valid_moves.values():
                    start_counter = counter    
                    temp_board.make_move(kill_position[0],kill_position[1],move[0],move[1])
                    self.auxiliary_recursive_function(move[0],move[1],color,temp_board,possible_sequential_kills)
                    counter = len(possible_sequential_kills)                    
                    #print("start_counter: ",start_counter)
                    #print("counter: ",counter)
                    for i in range(start_counter,counter):
                        possible_sequential_kills[i].append([move[0],move[1]]) 
                        possible_sequential_kills[i].append([kill_position[0],kill_position[1]])
            for i in range(len(possible_sequential_kills)):
                possible_sequential_kills[i].reverse()    
            return True, possible_sequential_kills
        else: return False


    def auxiliary_recursive_function(self,row,col,color,temp_board,possible_sequential_kills):
        if(temp_board.kill_is_possible(color,False,row,col) != False):
            #temp_board.board_representation()
            valid_moves = temp_board.kill_is_possible(color,False,row,col)[1]
            print("valid_moves:",valid_moves)
            for move in valid_moves:
                temp_board.make_move(row,col,move[0],move[1],valid = True)
                #temp_board.board_representation()
                self.auxiliary_recursive_function(move[0],move[1],color,temp_board,possible_sequential_kills)
                temp_board.make_move(move[0],move[1],row,col,valid = True)
                #temp_board.board_representation()
                possible_sequential_kills[len(possible_sequential_kills)-1].append([move[0],move[1]])
                  
        else:
            #print("end position")
            #print(row,' ',col)
            possible_sequential_kills.append([])
    #this function we need to control non-avoidance of possible kills
    #this means that if there is red's turn and on the current board exists movement
    #thet red piece can kill blue piece, then red can only make this movement
    def kill_is_possible(self,color,first_kill = True,row = None,col = None):
        #if color is red,we should check possible moves for all red pieces and 
        #if killing is possible, then discover which piece can kill
        kill_is_possible = False
        killing_positions = []
        if first_kill:
            for row in range(ROWS):
                for col in range(COLS):
                    if(self.board[row][col].piece != None):
                        if(self.board[row][col].piece.color == color):
                            valid_squares = self.valid_squares_to_move(row,col)
                            if "UpLeftKill" in valid_squares or "UpRightKill" in valid_squares or "DownRightKill" in valid_squares or "DownLeftKill" in valid_squares:
                                kill_is_possible = True
                                killing_positions.append([row,col])
        if not first_kill:
            if row-2>=0 and col+2<=7: 
                if self.board[row-1][col+1].piece != None:
                    if self.board[row-1][col+1].piece.color != color and self.board[row-2][col+2].piece == None:
                        kill_is_possible = True
                        killing_positions.append([row-2,col+2])
            if row+2<=7 and col+2<=7: 
                if self.board[row+1][col+1].piece != None:
                    if self.board[row+1][col+1].piece.color != color and self.board[row+2][col+2].piece == None:
                        kill_is_possible = True
                        killing_positions.append([row+2,col+2])
            if row+2<=7 and col-2>=0: 
                if self.board[row+1][col-1].piece != None:
                    if self.board[row+1][col-1].piece.color != color and self.board[row+2][col-2].piece == None:
                        kill_is_possible = True
                        killing_positions.append([row+2,col-2])
            if row-2>=0 and col-2>=0: 
                if self.board[row-1][col-1].piece != None:
                    if self.board[row-1][col-1].piece.color != color and self.board[row-2][col-2].piece == None:
                        kill_is_possible = True
                        killing_positions.append([row-2,col-2])
        if(kill_is_possible): return True, killing_positions
        else: return False
    
   #terminal state function
    def is_win(self):
        for i in range(COLS):
            if self.board[0][i].piece != None and self.board[0][i].piece.color == RED:
                return True
            if self.board[7][i].piece != None and self.board[7][i].piece.color == BLUE:
                return True
        return False
    
    def generate_states(self,color):
        #this is list of next possible states
        actions = []
        kills = self.sequential_kills_possible(color)
        if kills != False:
           for way in kills[1]:
                temp_board = copy.deepcopy(self)
                for index in range(len(way)-1):
                    if index != 0:   
                        temp_board.make_move(way[index][0],way[index][1],way[index+1][0],way[index+1][1],valid=True)
                    else:
                        temp_board.make_move(way[index][0],way[index][1],way[index+1][0],way[index+1][1])
                actions.append(temp_board)
        else:
            for row in range(ROWS):
                for col in range(COLS):
                    if(self.board[row][col].piece!= None and self.board[row][col].piece.color == color):
                        valid_actions = self.valid_squares_to_move(row,col)
                        if(valid_actions):
                            for position in valid_actions.values():
                                temp_board = copy.deepcopy(self)
                                temp_board.make_move(row,col,position[0],position[1])
                                actions.append(temp_board)
        #for state in actions:
        #    state.board_representation()
        #    print()
        return actions
    
    
    def perform_next_action(self,best_state):
        kills = self.sequential_kills_possible(BLUE)
        print(self.sequential_kills_possible(BLUE))
        if kills != False:
            for way in kills[1]:
                temp_board = copy.deepcopy(self)
                for index in range(len(way)-1):
                    if index != 0:   
                        temp_board.make_move(way[index][0],way[index][1],way[index+1][0],way[index+1][1],valid=True)
                    else:
                        temp_board.make_move(way[index][0],way[index][1],way[index+1][0],way[index+1][1])
                if best_state.board.string_repr() == temp_board.string_repr():
                    temp_board = copy.deepcopy(self)
                    for index in range(len(way)-1):
                        if index != 0:   
                            temp_board.make_move(way[index][0],way[index][1],way[index+1][0],way[index+1][1],WIN,valid=True)
                        else:
                            temp_board.make_move(way[index][0],way[index][1],way[index+1][0],way[index+1][1],WIN)
                        time.sleep(1)

                    return
        else:
            for row in range(ROWS):
                for col in range(COLS):
                    if(self.board[row][col].piece!= None and self.board[row][col].piece.color == BLUE):
                        valid_actions = self.valid_squares_to_move(row,col)
                        if(valid_actions):
                            for position in valid_actions.values():
                                temp_board = copy.deepcopy(self)
                                temp_board.make_move(row,col,position[0],position[1])
                                                                
                                if best_state.board.string_repr() == temp_board.string_repr():
                                   temp_board = copy.deepcopy(self)
                                   time.sleep(1)
                                   temp_board.make_move(row,col,position[0],position[1],WIN)
                                   return
                
    
    def string_repr(self):
        #define board string representation
        board_string = ''
        for row in range(ROWS):
            for col in range(COLS):
                if(self.board[row][col].piece != None):
                    board_string+=" "
                    board_string += f"rgb{self.board[row][col].piece.color}"
                    board_string+=" "
                else:
                    board_string+=" emptySquare "
        return board_string    
def cleaning_old(board,list_for_possible_moves):
        for way in list_for_possible_moves:  
                        i = 1
                        while(i<len(way)):
                            pygame.draw.circle(WIN,BLACK,((way[i][1]* SQUARE_SIZE) + SQUARE_SIZE //2 ,(way[i][0]* SQUARE_SIZE) + SQUARE_SIZE//2), 10)
                            i+=1

def main(): 
    
    run = True
    clock = pygame.time.Clock()
    board = Board(WIN)
    click_list = []   
    potential_moves = []    
    #We use movemement_count to discover who's turn is,if movement_count%2 == 0 then it's red's turn,otherwise blue's turn
    movement_count = 0
    click_count = 1
    list_for_possible_moves = []
    killing = False
    killing_started = False
    kill_but_not_first = False
    mcts = MCTS()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if(pygame.mouse.get_pressed()[0]):
                
                movement_done = False
                print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
                print("click count: ",click_count)
                cl_row, cl_col = get_row_col_with_mouse_pos(pygame.mouse.get_pos())
                if(click_count == 1 and board.board[cl_row][cl_col].piece == None and not list_for_possible_moves):continue
                if(board.board[cl_row][cl_col].piece != None):
                    if(movement_count % 2 == 0  and board.board[cl_row][cl_col].piece.color != RED):continue
                if(board.board[cl_row][cl_col].piece != None):
                    if(movement_count % 2 == 1  and board.board[cl_row][cl_col].piece.color != BLUE):continue
                
                print("list_for_possible_moves: ", list_for_possible_moves)
                print("potential_moves: ",potential_moves)
                
                invalid_click = False
                print(movement_count)
                if list_for_possible_moves :
                    squares_to_move_from = []
                    for way in list_for_possible_moves:
                        if way[0] not in squares_to_move_from:
                            squares_to_move_from.append(way[0])
                    print("squares to move from: ",squares_to_move_from)
                    print([cl_row,cl_col])
                    if [cl_row,cl_col] not in squares_to_move_from and [cl_row,cl_col] not in potential_moves:
                        invalid_click = True
                    if invalid_click:
                        cleaning_old(board,list_for_possible_moves)
                        break
                    
                    if potential_moves:
                        if [cl_row,cl_col] not in squares_to_move_from:
                            
                            if [cl_row,cl_col] not in potential_moves :
                                invalid_click = True
                            else:
                                index = 0
                                for way in list_for_possible_moves:
                                    if(way[1] == [cl_row,cl_col]):
                                        cleaning_old(board,list_for_possible_moves)    
                                        break
                                    index += 1
                                if list_for_possible_moves[index][0] != click_list[-1]:
                                    invalid_click = True
                                if invalid_click:
                                    cleaning_old(board,list_for_possible_moves)    
                                    break
                
                click_count += 1
                click_list.append([cl_row,cl_col]) 
                print(click_list)
                print("potential moves here:",potential_moves)
                
                for move in potential_moves:
                    pygame.draw.circle(WIN,BLACK,((move[1]* SQUARE_SIZE) + SQUARE_SIZE //2 ,(move[0]* SQUARE_SIZE) + SQUARE_SIZE//2), 10)
                print("killing here : ",killing)
                if(killing and movement_count%2 != 0):
                    cleaning_old(board,list_for_possible_moves)  
                if(click_list[-1] in potential_moves):
                    #print("here we are")    
                    board.make_move(click_list[-2][0],click_list[-2][1],click_list[-1][0],click_list[-1][1],WIN,valid=kill_but_not_first)  
                    movement_done = True
                    if(board.is_win()):
                        print("RED won the game!!!!!!!!") 
                        pygame.quit()

                    movement_count += 1
                potential_moves.clear()
                print("movement_done: ",movement_done)
                if(board.board[cl_row][cl_col].piece!= None):
                    if(not movement_done):
                        if(killing):
                            valid_squares_to_move_from = []
                            i = 1
                            for way in list_for_possible_moves:
                                valid_squares_to_move_from.append(way[0]) 
                                potential_moves.append(way[1])
                                i+=1
                            
                            #pygame.draw.rect(WIN,GREY,(cl_col*SQUARE_SIZE,cl_row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
                            #pygame.draw.circle(WIN,board.board[cl_row][cl_col].piece.color,(cl_col*SQUARE_SIZE + SQUARE_SIZE//2,cl_row*SQUARE_SIZE + SQUARE_SIZE//2),SQUARE_SIZE//2-10)
                            
                            for way in list_for_possible_moves:
                                if(way[0] == [cl_row,cl_col]):
                                    i = 1
                                    while(i<len(way)):
                                        pygame.draw.circle(WIN,GREY,((way[i][1]* SQUARE_SIZE) + SQUARE_SIZE //2 ,(way[i][0]* SQUARE_SIZE) + SQUARE_SIZE//2), 10)
                                        i+=1
                                
                        if(not killing):
                            valid_moves = board.valid_squares_to_move(cl_row,cl_col)
                            for moves in valid_moves.values():
                                potential_moves.append([moves[0],moves[1]])
                                pygame.draw.circle(WIN,GREY,((moves[1]* SQUARE_SIZE) + SQUARE_SIZE //2 ,(moves[0]* SQUARE_SIZE) + SQUARE_SIZE//2), 10)
                
                print("movement_done: ",movement_done)
                if(movement_done):
                    if list_for_possible_moves:
                        for way in list_for_possible_moves:
                            if(way[1]!=[cl_row,cl_col]):
                                list_for_possible_moves.remove(way)
                        for index in range(len(list_for_possible_moves)):
                            list_for_possible_moves[index].pop(0)
                        for way in list_for_possible_moves:
                            if(len(way) == 1):list_for_possible_moves.remove(way)    
                    if list_for_possible_moves:
                        kill_but_not_first = True    
                        movement_count -= 1
                    else:
                        kill_but_not_first= False    
                        if(board.board[cl_row][cl_col].piece.color == RED):
                            calling  = board.sequential_kills_possible(BLUE)
                            if(calling != False):
                                killing = True
                                list_for_possible_moves = calling[1]
                            else:killing = False
                        if(board.board[cl_row][cl_col].piece.color == BLUE):
                            calling  = board.sequential_kills_possible(RED)
                            if(calling != False):
                                killing = True
                                list_for_possible_moves = calling[1]
                            else:killing = False
                
                print("potential moves: ",potential_moves)
                print("click list : ",click_list)
                print("movement count: ",movement_count)
                
        pygame.display.update()     
        # Check if it's the computer's turn (BLUE side)
        if movement_count % 2 == 1:
           board.player = BLUE      
           best_move = mcts.search(board)
           board.perform_next_action(best_move)
           board = best_move.board
           kill_but_not_first = False
           board.player = RED      

           calling = board.sequential_kills_possible(RED)
           if(calling != False):
                killing = True
                list_for_possible_moves = calling[1]
           else:
               killing = False
               list_for_possible_moves=[]
           
           movement_count += 1    
           
        pygame.display.update()
    pygame.quit()
   
if __name__ == '__main__':
    main()


