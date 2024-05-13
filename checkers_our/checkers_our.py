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
            
    #get square which are legal to move current piece 
    def valid_squares_to_move(self,board):
        print("hi")
        valid_squares_row_col_dict = {}
        if(self.color == RED):
            if(board[self.row - 1][self.col + 1].piece == None):
                if(self.row - 1 >= 0 and self.row - 1 <= 8 and self.col + 1 >= 0 and self.col + 1 <= 8):
                    valid_squares_row_col_dict["UpRight"]=[self.row - 1, self.col + 1]
            elif(board[self.row - 1][self.col + 1].piece.color == BLUE and board[self.row - 2][self.col + 2].piece == None):
                if(self.row - 2 >= 0 and self.row - 2 <= 8 and self.col + 2 >= 0 and self.col + 2 <= 8):
                    valid_squares_row_col_dict["UpRightKill"]=[self.row - 2, self.col + 2]
            if(board[self.row - 1][self.col - 1].piece == None):
                if(self.row - 1 >= 0 and self.row - 1 <= 8 and self.col - 1 >= 0 and self.col - 1 <= 8):
                    valid_squares_row_col_dict["UpLeft"]=[self.row - 1, self.col - 1]
            elif(board[self.row - 1][self.col - 1].piece.color == BLUE and board[self.row - 2][self.col - 2].piece == None):
                if(self.row - 2 >= 0 and self.row - 2 <= 8 and self.col - 2 >= 0 and self.col - 2 <= 8):
                    valid_squares_row_col_dict["UpLeftKill"]=[self.row - 2, self.col - 2]
        if(self.color == BLUE):
            if(board[self.row + 1][self.col + 1].piece == None):
                if(self.row + 1 >= 0 and self.row + 1 <= 8 and self.col + 1 >= 0 and self.col + 1 <= 8):
                    valid_squares_row_col_dict["DownRight"]=[self.row + 1, self.col + 1]
            elif(board[self.row + 1][self.col + 1].piece.color == BLUE and board[self.row + 2][self.col + 2].piece == None):
                if(self.row + 2 >= 0 and self.row + 2 <= 8 and self.col + 2 >= 0 and self.col + 2 <= 8):
                    valid_squares_row_col_dict["DownRightKill"]=[self.row + 2, self.col + 2]
            if(board[self.row + 1][self.col - 1].piece == None):
                if(self.row + 1 >= 0 and self.row + 1 <= 8 and self.col - 1 >= 0 and self.col - 1 <= 8):
                    valid_squares_row_col_dict["DownLeft"]=[self.row + 1, self.col - 1]
            elif(board[self.row + 1][self.col - 1].piece.color == BLUE and board[self.row + 2][self.col + 2].piece == None): 
                if(self.row + 2 >= 0 and self.row + 2 <= 8 and self.col + 2 >= 0 and self.col + 2 <= 8):
                    valid_squares_row_col_dict["DownLeftKill"]=[self.row + 2, self.col + 2]       
        return valid_squares_row_col_dict
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
                    #self.board[i][j] = "BluePiece"
                    self.board[i][j].piece = Piece(i,j,BLUE)
                    self.board[i][j].piece.draw(win)
        for i in range(5,8):
            for j in range(COLS):
                if self.board[i][j].square_color == BLACK:
                    #self.board[i][j] = "RedPiece"
                    self.board[i][j].piece = Piece(i,j,RED)
                    self.board[i][j].piece .draw(win)
    '''
    def board_representation(self):
        print(''.join(f'{x:15}' for x in range(1,9)))
        for i in range(ROWS):
            print(i+1,'  ',end='')
            print(''.join(f'{x.color:15}' for x in self.board[i]))
    '''   
        
    def make_move(self,y1,x1,y2,x2,win):
        #If movement is legal than make move
        if self.is_legal_move(y1,x1,y2,x2):
           #Check if this movement is simple movement or killing opponent's piece
           #In any case we have to do one action similarly,and this action is after following if condition
           #But in case of killing, we have to do one additional action
           #We have to take opponent's piece from the board 
            if(abs(y2-y1) == 2):
                print("this is killing")
                  #detect location of opponent's piece
                if(y2>y1 and x2>x1):
                    self.board[y1+1][x1+1].square_color = BLACK
                    pygame.draw.rect(win, BLACK, ((x1+1) * SQUARE_SIZE,(y1+1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif(y2>y1 and x2<x1):
                    self.board[y1+1][x1-1].square_color = BLACK
                    pygame.draw.rect(win, BLACK, ((x1-1) * SQUARE_SIZE,(y1+1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif(y2<y1 and x2<x1):
                    self.board[y1-1][x1-1].square_color = BLACK
                    pygame.draw.rect(win, BLACK, ((x1-1) * SQUARE_SIZE,(y1-1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif(y2<y1 and x2>x1):
                    self.board[y1-1][x1+1].square_color = BLACK
                    pygame.draw.rect(win, BLACK, ((x1+1) * SQUARE_SIZE,(y1-1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            #this is simple movement,so we just have to swap values on the board's following locations[y1][x1] and [y2][y1] 
            self.board[y2][x2], self.board[y1][x1] = self.board[y1][x1], self.board[y2][x2]
            pygame.draw.rect(win, BLACK, (x1 * SQUARE_SIZE,y1 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if(self.board[y2][x2].piece.color == BLUE):
                Piece(y2,x2,BLUE).draw(win)
            if(self.board[y2][x2].piece.color == RED):
                Piece(y2,x2,RED).draw(win)
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
                print("move is not valid if it is not directed up with one or two squares")
                return False
            if y1 - y2 == 1:
                #move is not valid if difference between columns of previous and next positions is not equal to 1 
                print("y1 - y2 == 1")
                if(abs(x2 - x1) != 1):
                    print("abs(x2 - x1) != 1")
                    print("move is not valid if difference between columns of previous and next positions is not equal to 1")
                    return False
                else:
                    print("abs(x2 - x1) == 1")
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
def main(): 
    
    run = True
    clock = pygame.time.Clock()
    board = Board(WIN)
    click_list = []
   
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if(pygame.mouse.get_pressed()[0]):
                cl_row, cl_col = get_row_col_with_mouse_pos(pygame.mouse.get_pos())
                print(cl_row,' ',cl_col)
                if(board.board[cl_row][cl_col].piece!= None):
                    valid_moves = board.board[cl_row][cl_col].piece.valid_squares_to_move(board.board)
                    print(valid_moves)
                    for moves in valid_moves.values():
                        print(moves[0]+1,' ',moves[1]+1)
                        pygame.draw.circle(WIN,GREY,((moves[1]* SQUARE_SIZE) + SQUARE_SIZE //2 ,(moves[0]* SQUARE_SIZE) + SQUARE_SIZE//2), 10)
                    pygame.display.update()
                #click_list.append([cl_row,cl_col])
                #print(cl_row," ",cl_col)
                
               
                #print("make move ",click_list)
                #board.make_move(click_list[0][0],click_list[0][1],click_list[1][0],click_list[1][1],WIN)
                #click_list.clear()
                #board.board_representation()
                #break
            '''
            if event.type == pygame.MOUSEBUTTONDOWN and event.type == pygame.MOUSEBUTTONDOWN:
                pos1 = pygame.mouse.get_pos()
                row1, col1 = get_row_col_with_mouse_pos(pos1)
                pos2 = pygame.mouse.get_pos()
                row2, col2 = get_row_col_with_mouse_pos(pos2)
                board.make_move(row1,col1,row2,col2)
            '''
        
        pygame.display.update()
    pygame.quit()
    '''
    board = Board()
    board.board_representation()
    game_end = False
    while(not game_end):
        y1,x1 = input("Enter row and column of piece which you want to move seperated by space: ").split()
        y2,x2 = input("Enter row and column of location where you want to move this piece: ").split()
        print(board.make_move(int(y1)-1,int(x1)-1,int(y2)-1,int(x2)-1)) 
        board.board_representation()
        game_continue = input("If you want to end game print F:")
        if(game_continue == 'F'): game_end = True
    '''
if __name__ == '__main__':
    main()



