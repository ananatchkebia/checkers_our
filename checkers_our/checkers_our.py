from pickle import NONE
import pygame

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
    def make_move(self,y1,x1,y2,x2,win):
        #If movement is legal than make move
        if self.is_legal_move(y1,x1,y2,x2):
           #Check if this movement is simple movement or killing opponent's piece
           #In any case we have to do one action similarly,and this action is after following if condition
           #But in case of killing, we have to do one additional action
           #We have to take opponent's piece from the board 
            if(abs(y2-y1) == 2):
                print("this is killing")
                
                self.board[y1][x1].piece.killer = True
                  #detect location of opponent's piece
                if(y2>y1 and x2>x1):
                    self.board[y1+1][x1+1].square_color = BLACK
                    self.board[y1+1][x1+1].piece = None
                    pygame.draw.rect(win, BLACK, ((x1+1) * SQUARE_SIZE,(y1+1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif(y2>y1 and x2<x1):
                    self.board[y1+1][x1-1].square_color = BLACK
                    self.board[y1+1][x1-1].piece = None
                    pygame.draw.rect(win, BLACK, ((x1-1) * SQUARE_SIZE,(y1+1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif(y2<y1 and x2<x1):
                    self.board[y1-1][x1-1].square_color = BLACK
                    self.board[y1-1][x1-1].piece = None
                    pygame.draw.rect(win, BLACK, ((x1-1) * SQUARE_SIZE,(y1-1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif(y2<y1 and x2>x1):
                    self.board[y1-1][x1+1].square_color = BLACK
                    self.board[y1-1][x1+1].piece = None
                    pygame.draw.rect(win, BLACK, ((x1+1) * SQUARE_SIZE,(y1-1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            #this is simple movement,so we just have to swap values on the board's following locations[y1][x1] and [y2][y1] 
            self.board[y2][x2], self.board[y1][x1] = self.board[y1][x1], self.board[y2][x2]
            pygame.draw.rect(win, BLACK, (x1 * SQUARE_SIZE,y1 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if(self.board[y2][x2].piece.color == BLUE):
                Piece(y2,x2,BLUE).draw(win)
            if(self.board[y2][x2].piece.color == RED):
                Piece(y2,x2,RED).draw(win)
    def is_legal_move(self,y1,x1,y2,x2):
        for valid_square in self.valid_squares_to_move(y1,x1).values():
            if(valid_square[0] == y2 and valid_square[1] == x2):return True
        return False
    
    #this function we need to control non-avoidance of possible kills
    #this means that if there is red's turn and on the current board exists movement
    #thet red piece can kill blue piece, then red can only make this movement
    def possible_killing_positions(self,color):
        killing_positions = []
       
    def kill_is_possible(self,color):
        #if color is red,we should check possible moves for all red pieces and 
        #if killing is possible, then discover which piece can kill
        kill_is_possible = False
        killing_positions = []
        for row in range(ROWS):
            for col in range(COLS):
                if(self.board[row][col].piece != None):
                    if(self.board[row][col].piece.color == color):
                        valid_squares = self.valid_squares_to_move(row,col)
                        if "UpLeftKill" in valid_squares or "UpRightKill" in valid_squares or "DownRightKill" in valid_squares or "DownLeftKill" in valid_squares:
                            kill_is_possible = True
                            killing_positions.append([row,col])
        if(kill_is_possible): return True, killing_positions
        else: return False
        
    #def valid_kills(self):
        
    '''
    def is_legal_move(self,y1,x1,y2,x2):
        #check that destination is black_square(so this square is empty and available)
        if self.board[y2][x2].square_color != BLACK: 
            print(y2+1," ",x2+1," is not BlackSquare") 
            return False
        #check that movement is valid for non-queen piece
        if not self.legal_move_main_rule(y1,x1,y2,x2):return False
        return True
    def legal_move_main_rule(self,y1,x1,y2,x2):
        #if piece is red than it can move up-right or up-left
        if(self.board[y1][x1].piece.color == RED):
            print("you want to move red piece!")
            #move is not valid if it is not directed up with one or two squares
            if(y1 - y2 != 1 and y1 - y2 != 2):
                return False
            if y1 - y2 == 1:
                #move is not valid if difference between columns of previous and next positions is not equal to 1 
                if(abs(x2 - x1) != 1):
                    return False
                else:
                    return True
            #here already means that y2-y1=2,so this will be valid only in case of killing piece of opponent
            #so here we have to check two conditions:
            #one that difference between columns of previous and next positions is equal to 2
            #and second that between them is opponent's piece
            else:
                print("This is killing")
                if(abs(x2 - x1) != 2):return False
                if(x1 > x2):
                    if(self.board[y1-1][x1-1].piece.color != BLUE):return False
                else:
                    if(self.board[y1-1][x1+1].piece.color != BLUE):return False
                return True   
        #if piece is black than it can move down-right or down-left
        if(self.board[y1][x1].piece.color == BLUE):
            print("you want to move Blue piece!")
            #move is not valid if it is not directed down with one or two squares
            if(y2 - y1 != 1 and y2 - y1 != 2):return False
            if y2 - y1 == 1:
                #move is not valid if difference between columns of previous and next positions is not equal to 1 
                if(abs(x2 - x1) != 1):return False
                return True
            #here already means that y1-y2=2,so this will be valid only in case of killing piece of opponent
            #so here we have to check two conditions:
            #one that difference between columns of previous and next positions is equal to 2
            #and second that between them is opponent's piece
            else:
                print("this is killing")
                if(abs(x2 - x1) != 2): 
                    return False
                if(x1 > x2):
                    if(self.board[y1+1][x1-1].piece.color != RED):
                        return False
                else:
                    if(self.board[y1+1][x1+1].piece.color != RED):
                        return False
                return True
    '''    
def main(): 
    
    run = True
    clock = pygame.time.Clock()
    board = Board(WIN)
    click_list = []   
    potential_moves = []    
    movement_count = 0
    click_count = 0
    list_for_possible_moves = []
    killing = False
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if(pygame.mouse.get_pressed()[0]):
                movement_done = False
                print("click count: ",click_count)
                print("movement count: ",movement_count)
                cl_row, cl_col = get_row_col_with_mouse_pos(pygame.mouse.get_pos())
                #unda gavtesto click_count != 1
                if(click_count == 0 and board.board[cl_row][cl_col].piece == None and not list_for_possible_moves):continue
                if(board.board[cl_row][cl_col].piece != None):    
                    if(movement_count % 2 == 0  and board.board[cl_row][cl_col].piece.color != RED):continue
                if(board.board[cl_row][cl_col].piece != None):
                    if(movement_count % 2 == 1  and board.board[cl_row][cl_col].piece.color != BLUE):continue
                    
                if(board.board[cl_row][cl_col].piece != None ):
                    print("kill is possible: ",board.kill_is_possible(board.board[cl_row][cl_col].piece.color))                   
                    if(board.kill_is_possible(board.board[cl_row][cl_col].piece.color) != False):
                        print(board.kill_is_possible(board.board[cl_row][cl_col].piece.color))
                        killing = True
                        list_for_possible_moves = board.kill_is_possible(board.board[cl_row][cl_col].piece.color)[1]
                    else:killing = False
                        


                print("list_for_possible_moves: ", list_for_possible_moves)
                print("potential_moves: ",potential_moves)
                
                if list_for_possible_moves:
                    if([cl_row,cl_col] in potential_moves):
                        for move in potential_moves:
                            pygame.draw.circle(WIN,BLACK,((move[1]* SQUARE_SIZE) + SQUARE_SIZE //2 ,(move[0]* SQUARE_SIZE) + SQUARE_SIZE//2), 10)
                        square_to_move_from = None
                        for square in list_for_possible_moves:
                            if([cl_row,cl_col] in board.valid_squares_to_move(square[0],square[1]).values()):
                                square_to_move_from = square
                                board.make_move(square[0],square[1],cl_row,cl_col,WIN)
                                movement_count += 1
                                movement_done = True
                        for element in list_for_possible_moves:
                                pygame.draw.rect(WIN,BLACK,(element[1]*SQUARE_SIZE,element[0]*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
                                if(element == square_to_move_from): continue
                                pygame.draw.circle(WIN,GREY,(element[1]*SQUARE_SIZE + SQUARE_SIZE//2,element[0]*SQUARE_SIZE + SQUARE_SIZE//2),SQUARE_SIZE//2 - 8)
                                pygame.draw.circle(WIN,board.board[cl_row][cl_col].piece.color,(element[1]*SQUARE_SIZE + SQUARE_SIZE//2,element[0]*SQUARE_SIZE + SQUARE_SIZE//2),SQUARE_SIZE//2 - 10)
                        list_for_possible_moves.clear()
                        potential_moves.clear()

                
                        
                if(not killing):
                    click_list.append([cl_row,cl_col])
                    click_count += 1
                
                            
                    for move in potential_moves:
                        pygame.draw.circle(WIN,BLACK,((move[1]* SQUARE_SIZE) + SQUARE_SIZE //2 ,(move[0]* SQUARE_SIZE) + SQUARE_SIZE//2), 10)
                
                    if(click_list[-1] in potential_moves):
                        board.make_move(click_list[-2][0],click_list[-2][1],click_list[-1][0],click_list[-1][1],WIN)  
                        movement_done = True
                        movement_count += 1
                        click_count = 0
                        #print("This is killer:",board.board[cl_row][cl_col].piece.killer)
                    potential_moves.clear()
                    board.board_representation()
                
                if(board.board[cl_row][cl_col].piece!= None):
                    if(not movement_done):
                        valid_moves = board.valid_squares_to_move(cl_row,cl_col)
                        print(valid_moves)
                        
                        #here I am trying to remove all potential moves except killing
                        if(killing):
                            valid_moves.clear()
                            i = 1
                            for element in list_for_possible_moves:
                                valid_moves[i] = (board.valid_squares_to_move(element[0],element[1]))
                                i += 1
                            print(valid_moves)
                            valid_moves = {outer_key: {inner_key: value for inner_key, value in inner_dict.items() if "Kill" in inner_key}for outer_key, inner_dict in valid_moves.items()}
                            print(valid_moves)
                            #{1: {'DownRightKill': [4, 4]}, 2: {'DownLeftKill': [4, 2]}}
                            for j in range(1,i):
                                inner_dict = valid_moves[j]
                                for piece in inner_dict.values():
                                    potential_moves.append([piece[0],piece[1]])
                            print("list_for_possible_moves:",list_for_possible_moves)
                            for element in list_for_possible_moves:
                                pygame.draw.rect(WIN,GREY,(element[1]*SQUARE_SIZE,element[0]*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
                                pygame.draw.circle(WIN,board.board[element[0]][element[1]].piece.color,(element[1]*SQUARE_SIZE + SQUARE_SIZE//2,element[0]*SQUARE_SIZE + SQUARE_SIZE//2),SQUARE_SIZE//2 - 10)

                            for move in potential_moves:
                                pygame.draw.circle(WIN,GREY,((move[1]* SQUARE_SIZE) + SQUARE_SIZE //2 ,(move[0]* SQUARE_SIZE) + SQUARE_SIZE//2), 10)
                                
                        if(not killing):
                            for moves in valid_moves.values():
                                potential_moves.append([moves[0],moves[1]])
                                pygame.draw.circle(WIN,GREY,((moves[1]* SQUARE_SIZE) + SQUARE_SIZE //2 ,(moves[0]* SQUARE_SIZE) + SQUARE_SIZE//2), 10)
                        
                            
                print("potential moves: ",potential_moves)
                print("click list: ",click_list)
                
            
        
        pygame.display.update()
    pygame.quit()
   
if __name__ == '__main__':
    main()



