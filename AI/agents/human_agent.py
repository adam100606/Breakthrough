from BreakThrough import BreakThrough
import pygame
from graphics import *
from junk import *
class human_agent:
    LST = []
    def __init__(self, player, env: BreakThrough, graphics: Graphics):
        self.env = env
        self.player = player
        self.graphics = graphics


    def get_action(self,sta = None):
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if len(self.LST) == 2:
                RP,CP = self.LST[0]
                RT,CT = self.LST[1]
                
                if (RP-RT)*self.player == 1:
                    if   0 <= CT<=7:
                        if CP - CT == 1:
                            if self.env.is_legal(self.env.state,((RP,CP),dia_left)):
                                return ((RP,CP),dia_left)
                                
                        elif CP - CT == -1:
                            if self.env.is_legal(self.env.state,((RP,CP),dia_right)):
                                return ((RP,CP),dia_right)
                            
                        elif CP - CT == 0:
                            if self.env.is_legal(self.env.state,((RP,CP),forward)):
                                return ((RP,CP),forward)
                            
                        self.LST = []
                        break
                    self.LST = []
                self.LST = []
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                RP,CP = self.graphics.nevo(pos)
                self.LST.append((RP,CP))
                
                # self.graphics.mark_square((RP,CP),green)
                
                
               
                
                            
                                




                
        return None
    def __call__(self, events):
        return self.get_action(events)
    