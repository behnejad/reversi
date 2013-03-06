import kivy
kivy.require('1.1.1')

import copy
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.properties import ObjectProperty
from board import Board, move_string, print_moves


# a simple solution for the data. not the brightest one. anyone who wants
# something else should do it himself.

class KherseKhasteWidget(Widget):
    
    started = False #determines whether the game is started or not
    level = 0 #current level
    random = False #if the level is random...
    board = Board() #the game board
    
    def update_screen(self):
        '''updated the screen'''
        #we redraw everything at each update so that the game can support them rotation of the device
        with self.canvas:
            self.canvas.clear()
            #TODO: this is just a placeholder. load the board from an image file.
            for j in range(7,-1,-1):
                for i in range(8):
                    Color(0.2, 0.85, 0.2)
                    Rectangle(pos=[self.pos[0] + 2 + 
                    (i * self.size[0] / 8.0), self.pos[1] + 2 + (j * self.size[1] / 8.0)]
                    , size=[self.size[0] / 8.0 - 4, self.size[1] / 8.0 - 4])
                    if (self.board[i][j] == 1):
                        Color(0.9, 0.9, 0.9)
                        Ellipse(pos=[self.pos[0] + 2 + (i * self.size[0] / 8.0),
                                     self.pos[1] + 2 + (j * self.size[1] / 8.0)]
                                    , size=[self.size[0] / 8.0 - 4, self.size[1] / 8.0 - 4])
                    elif (self.board[i][j] == -1):
                        Color(0.1, 0.1, 0.1)
                        Ellipse(pos=[self.pos[0] + 2 + (i * self.size[0] / 8.0),
                                     self.pos[1] + 2 + (j * self.size[1] / 8.0)]
                                    , size=[self.size[0] / 8.0 - 4, self.size[1] / 8.0 - 4])
                        
    def on_touch_down(self, touch):
        '''handles the touch event'''
        if (not self.started):
            self.started = True
            self.update_screen()
            
        
class KherseKhasteApp(App):
    def build(self):
        return KherseKhasteWidget() #start the game

if __name__ == '__main__':
    KherseKhasteApp().run()
