import kivy
kivy.require('1.1.1')

import copy
import random
from copy import deepcopy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.properties import ObjectProperty
from board import Board, move_string, print_moves

class RandomEngine:
    def moving(self, board, color, moves):
        return random.choice(moves)

class Easy_AI: #gharche kheng
    def moving(self, board, color, moves):
        l = moves
        for i in l:
            if i == (0,0):
                return (0,0)
            if i == (0,7):
                return (0,7)
            if i == (7,7):
                return (7,7)
            if i == (7,0):
                return (7,0)
        return random.choice(l)

class Normal_AI: #maare divooneh
    def moving(self, board, color, moves):
        score = []
        for move in moves:
            mscore = 0
            new_board = deepcopy(board)
            new_board.execute_move(move, color)
            mscore += new_board.count(color) - board.count(color)
            if (move == (0,0) or move == (0,7) or move == (7,0) or move == (7,7)):
                mscore += 16
            if (move[0] == 0 or move[0] == 7 or move[1] == 0 or move[1] == 7):
                mscore += 8
            new_moves = new_board.get_legal_moves(-color)
            very_bad = [(0,0),(0,7),(7,0),(7,7)]
            for n in very_bad:
                if (n in new_moves):
                    mscore -= 10
            bad = deepcopy(very_bad)
            for i in [1,2,3,4,5,6]:
                bad.append((0,i))
                bad.append((7,i))
                bad.append((i,0))
                bad.append((i,7))
            for n in bad:
                if (n in new_moves):
                    mscore -= 2
            if (len(new_moves) == 0):
                mscore += 24
            mscore -= int(len(new_moves) / 5)
            score.append(mscore)
        return moves[score.index(max(score))]
    
class KherseKhasteWidget(Widget):

    mode = 0 # 0 : Human-vs-Human      1 : Computer-vs-Human
    current = 1 # current player. -1 : black, 1 : white
    started = False #determines whether the game is started or not
    random = False #if the level is random...
    board = Board() #the game board
    AI_engine = Normal_AI()#TODO: after we get our diverse AIs, we should be able to select one.
 
    def end_game(self): #TODO: a screen proclaiming the winner and the scores
        exit()
	
    def get_AI_next_move(self, engine, board, color):
        return engine.moving(board, color, self.board.get_legal_moves(color))
	
    def update_screen(self):
        '''updated the screen'''
        #we redraw everything at each update so that the game can support the rotation of the device
        with self.canvas:
            self.canvas.clear()
            #TODO: --- Reza --- this is just a placeholder. load the board from an image file. --- Reza ---
            for j in range(7,-1,-1):
                for i in range(8):
                    Color(0.2, 0.85, 0.2)
                    Rectangle(pos=[self.pos[0] + 2 + 
                    (i * self.size[0] / 8.0), self.pos[1] + 2 + (j * self.size[1] / 8.0)]
                    , size=[self.size[0] / 8.0 - 4, self.size[1] / 8.0 - 4])
                    if (self.board[i][j] == 1):
                        Color(0.9, 0.9, 0.9) #White
                        Ellipse(pos=[self.pos[0] + 2 + (i * self.size[0] / 8.0),
                                     self.pos[1] + 2 + (j * self.size[1] / 8.0)]
                                    , size=[self.size[0] / 8.0 - 4, self.size[1] / 8.0 - 4])
                    elif (self.board[i][j] == -1):
                        Color(0.1, 0.1, 0.1) #Black
                        Ellipse(pos=[self.pos[0] + 2 + (i * self.size[0] / 8.0),
                                     self.pos[1] + 2 + (j * self.size[1] / 8.0)]
                                    , size=[self.size[0] / 8.0 - 4, self.size[1] / 8.0 - 4])
                    if ((i, j) in self.board.get_legal_moves(self.current)):
                        Color(0.3, 0.9, 0.3) #Legal moves
                        Ellipse(pos=[self.pos[0] + 2 + (i * self.size[0] / 8.0),
                                     self.pos[1] + 2 + (j * self.size[1] / 8.0)]
                                    , size=[self.size[0] / 8.0 - 4, self.size[1] / 8.0 - 4])
                        
    def translate_touch(self, touch):
        '''returning the proper behaviour after we touched the screen'''
        x = int (touch.x / self.size[0] * 8.0)
        y = int (touch.y / self.size[1] * 8.0)
        if (self.mode == 0): #both are humans
            if ((x, y) in self.board.get_legal_moves(self.current)):
                self.board.execute_move((x, y), self.current)
                if (len(self.board.get_legal_moves(1)) == 0 and len(self.board.get_legal_moves(-1)) == 0):
                    self.end_game()
                if (len(self.board.get_legal_moves(-self.current)) != 0):
                    self.current = - self.current
                self.update_screen()
        elif (self.mode == 1): #one is AI
            if ((x, y) in self.board.get_legal_moves(self.current)):
                self.board.execute_move((x, y), self.current)
                if (len(self.board.get_legal_moves(1)) == 0 and len(self.board.get_legal_moves(-1)) == 0):
                    exit()
                self.update_screen()
                if (len(self.board.get_legal_moves(-self.current)) != 0): #we must make sure that the AI will be able to excute a move before assigning the game 
                    self.current = - self.current
                else:
                    return
                while 1:# do this until human player has moves available
                    self.board.execute_move(self.get_AI_next_move(self.AI_engine, self.board, (-1)), self.current)
                    if (len(self.board.get_legal_moves(1)) == 0 and len(self.board.get_legal_moves(-1)) == 0):
                        self.end_game()
                    if (len(self.board.get_legal_moves(-self.current)) != 0):
                        self.current = - self.current
                        self.update_screen()
                        break

    
    def on_touch_down(self, touch):
        '''handles the touch event'''
        if (not self.started):
            self.started = True
            self.current = 1
            if (touch.y / self.size[1] < 0.5):
                self.mode=0
            else:
                self.mode=1
            self.update_screen()
        else:
            self.translate_touch(touch)
                

        
        
class KherseKhasteApp(App):
    def build(self):
        return KherseKhasteWidget() #start the game

if __name__ == '__main__':
    KherseKhasteApp().run()
