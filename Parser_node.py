from Scanner import *
from Token import *

OperatorTokenType = { TokenType.PLUS,
                        TokenType.MINUS,
                        TokenType.MUL,
                        TokenType.DIV,
                        TokenType.POWER
                        }

class ExprNode(object):
    def __init__(self,item):
        self.item = item
        if self.item in OperatorTokenType:
            self.left = None
            self.right = None
        elif self.item == TokenType.FUNC:
            self.funcptr = None
            self.middle = None
        self.value = None
    
    def __str__(self):
        return str(self.item)
    
    def GetValue(self):
        if self.item == TokenType.PLUS:
            self.value = self.left.value + self.right.value
        elif self.item == TokenType.MINUS:
            self.value = self.left.value - self.right.value
        elif self.item == TokenType.MUL:
            self.value = self.left.value * self.right.value
        elif self.item == TokenType.DIV:
            self.value = self.left.value / self.right.value
        elif self.item == TokenType.POWER:
            self.value = self.left.value ** self.right.value
        elif self.item == TokenType.FUNC:
            self.value = self.funcptr(self.middle.value)
        return self.value
