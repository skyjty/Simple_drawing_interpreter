from Parser_process import *
from Scanner import *
from Token import *

import numpy as np
import matplotlib.pyplot as plt
import os

class Semantic(Parser):
    def init(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

    def calc(self, x, y):
        x *= self.x_scale
        y *= self.y_scale
        temp1 = x * np.cos(self.rot) + y * np.sin(self.rot)
        y = y * np.cos(self.rot) - x * np.sin(self.rot) #修复逻辑问题
        x = temp1
        x += self.x_origin
        y += self.y_origin
        return x, y
    
    def Draw(self):
        x, y = self.calc(self.x_ptr, self.y_ptr)
        color_normalized = [(c % 256) / 255 for c in self.color]    #处理不在[0,255]的常量
        self.ax.scatter(x, y, color=color_normalized)

    def Statement(self):        # 为每一个语句转进每一种文法
        self.enter("Statement")
        if self.token.type == TokenType.ORIGIN:
            self.OriginStatement()
        elif self.token.type == TokenType.SCALE:
            self.ScaleStatement()
        elif self.token.type == TokenType.FOR:
            self.ForStatement()
            self.Draw()
        elif self.token.type == TokenType.ROT:
            self.RotStatement()
        elif self.token.type == TokenType.COLOR:
            self.ColorStatement()
        elif self.token.type == TokenType.CONST_ID or self.token.type == TokenType.L_BRACKET or self.token.type == TokenType.MINUS:
            self.Expression()
        else:
            self.log(f"{self.token.type}")
            self.log(f"ERROR in line {self.scanner.line_num}, Error Mark: {self.token.lexeme}")
            # sys.exit(1)
        self.back("Statement")

    def Parser(self):
        self.enter("Parser")
        if self.scanner.s_ptr is None:
            self.log(f"Empty Input.")
        else:
            self.FetchToken()
            self.Program()
            # plt.show()
            self.scanner.CloseScanner()
            self.back("Parser")

    def SaveFig(self,save_path):
        self.fig.savefig(save_path)

    def ShowFig(self):
        self.fig.show()