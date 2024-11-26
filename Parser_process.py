import numpy as np
import sys
from Parser_node import *
from Scanner import *
# from Token import *

class Parser(object):
    def __init__(self,scanner):
        self.scanner = scanner
        self.token = None
        self.Parameter = 0
        self.x_origin = 0
        self.y_origin = 0
        self.x_scale = 1
        self.y_scale = 1
        self.rot = 0
        self.x_ptr = None
        self.y_ptr = None
        self.Tvalue = 0
        self.ParserOutput = ''
        self.color = [0,0,0]

    def error_exit(self,error_num):
        self.log(f"Quit with error num {error_num}.")
        sys.exit(1)

    def enter(self,x):
        self.log(f"Enter {x}")

    def back(self,x):
        self.log(f"Exit {x}")

    def call_match(self,x):
        self.log(f"Match Token {x}")

    def ShowTree(self,x):
        self.PrintTree(x,1)

    def FetchToken(self):
        self.token = self.scanner.GetToken()
        while self.token.type == TokenType.NONTOKEN:
            self.token = self.scanner.GetToken()
        if self.token == TokenType.ERRTOKEN:
            self.log(f"{self.token.type}")
            self.log(f"ERROR in line {self.scanner.line_num}, Error Mark: {self.token.lexeme}")
            # sys.exit(1)

    def MatchToken(self,token_type):
        if self.token.type != token_type:
            self.log(f"{self.token.type}")
            self.log(f"ERROR in line {self.scanner.line_num}, Error Mark: {self.token.lexeme}")
            # sys.exit(1)
        
        if  token_type == TokenType.SEMICO:
            self.scanner.s_ptr.readline()
            last = self.scanner.s_ptr.tell()
            next_line = self.scanner.s_ptr.readline()
            if len(next_line) == 0:
                return
            else:
                self.scanner.s_ptr.seek(last)
        self.FetchToken()

    def PrintTree(self,root,indent):
        for i in range(indent):
            self.log('\t', newline=False)

        if root.item == TokenType.PLUS:
            self.log(f"+ ")
        elif root.item == TokenType.MINUS:
            self.log(f"- ")
        elif root.item == TokenType.MUL:
            self.log(f"* ")
        elif root.item == TokenType.DIV:
            self.log(f"/ ")
        elif root.item == TokenType.POWER:
            self.log(f"** ")
        elif root.item == TokenType.FUNC:
            self.log(f"{root.funcptr}")
        elif root.item == TokenType.CONST_ID:
            self.log(f"{root.value:.5f}")
        #ADD BY SKY
        elif root.item == TokenType.CONST_COL:
            self.log(f"[{', '.join(f'{v:.5f}' if isinstance(v, (int, float)) else str(v) for v in root.value)}]")
        elif root.item == TokenType.T:
            self.log(f"{root.value}")
        else:
            print("ERROR Node Type")
            self.log(f"ERROR Node Type")
            # sys.exit(0)
        if root.item == TokenType.CONST_ID or root.item == TokenType.CONST_COL or root.item == TokenType.T:
            return          # 常数和参数是叶子节点
        elif root.item == TokenType.FUNC:
            self.PrintTree(root.middle, indent + 1)   # 函数只有一个孩子节点
        else:               # 先序遍历
            self.PrintTree(root.left, indent + 1)
            self.PrintTree(root.right, indent + 1)

    def Parser(self):
        self.enter("Parser")
        if self.scanner.s_ptr is None:
            print("Empty Input")
            self.log(f"Empty Input")
        else:
            self.FetchToken()
            self.Program()
            self.back("Parser")

    def Program(self):
        self.enter("Program")
        while self.token.type != TokenType.SEMICO:
            self.Statement()
            self.MatchToken(TokenType.SEMICO)
            self.call_match("; ")
        self.back("Program")
    
    def Statement(self):        # 为每一个语句转进每一种文法
        self.enter("Statement")
        if self.token.type == TokenType.ORIGIN:
            self.OriginStatement()
        elif self.token.type == TokenType.SCALE:
            self.ScaleStatement()
        elif self.token.type == TokenType.FOR:
            self.ForStatement()
        elif self.token.type == TokenType.ROT:
            self.RotStatement()
        # ADD BY SKY
        elif self.token.type == TokenType.COLOR:
            self.ColorStatement()
        elif self.token.type == TokenType.CONST_ID or self.token.type == TokenType.L_BRACKET or self.token.type == TokenType.MINUS:
            self.Expression()
        else:
            self.log(f"{self.token.type}")
            self.log(f"ERROR in line {self.scanner.line_num}, Error Mark: {self.token.lexeme}")
            # sys.exit(1)
        self.back("Statement")

    def OriginStatement(self):      # origin语句
        self.enter("OriginStatement")
        self.MatchToken(TokenType.ORIGIN)
        self.call_match("ORIGIN")
        self.MatchToken(TokenType.IS)
        self.call_match("IS")
        self.MatchToken(TokenType.L_BRACKET)
        self.call_match("(")
        temp = self.Expression()
        self.x_origin = temp.GetValue()
        self.MatchToken(TokenType.COMMA)
        self.call_match(",")
        temp = self.Expression()
        self.y_origin = temp.GetValue()
        self.MatchToken(TokenType.R_BRACKET)
        self.call_match(")")
        self.back("OriginStatement")

    def ScaleStatement(self):   # scale语句
        self.enter("ScaleStatement")
        self.MatchToken(TokenType.SCALE)
        self.call_match("SCALE")
        self.MatchToken(TokenType.IS)
        self.call_match("IS")
        self.MatchToken(TokenType.L_BRACKET)
        self.call_match("(")
        temp = self.Expression()
        self.x_scale = temp.GetValue()

        self.MatchToken(TokenType.COMMA)
        self.call_match(",")
        temp = self.Expression()
        self.y_scale = temp.GetValue()

        self.MatchToken(TokenType.R_BRACKET)
        self.call_match(")")
        self.back("ScaleStatement")

    def ColorStatement(self):   # color语句
        self.enter("ColorStatement")
        self.MatchToken(TokenType.COLOR)
        self.call_match("COLOR")
        self.MatchToken(TokenType.IS)
        self.call_match("IS")

        self.ColorExpression()

        self.back("ColorStatement")

    def ColorExpression(self):
        self.enter("ColorExpression")
        if self.token.type == TokenType.CONST_COL:
            temp = self.token.value
            self.MatchToken(TokenType.CONST_COL)
            address = self.GeneratNode_CONST_COL(TokenType.CONST_COL, temp)
            self.ShowTree(address)
            self.color = temp
        else:
            self.MatchToken(TokenType.L_BRACKET)
            self.call_match("(")

            temp = self.Expression()
            self.color[0] = temp.GetValue()
            self.MatchToken(TokenType.COMMA)
            self.call_match(",")
            
            temp = self.Expression()
            self.color[1] = temp.GetValue()
            self.MatchToken(TokenType.COMMA)
            self.call_match(",")

            temp = self.Expression()
            self.color[2] = temp.GetValue()

            self.MatchToken(TokenType.R_BRACKET)
            self.call_match(")")
        self.back("ColorExpression")

    def RotStatement(self):     # rot语句
        self.enter("RotStatement")
        self.MatchToken(TokenType.ROT)
        self.call_match("ROT")
        self.MatchToken(TokenType.IS)
        self.call_match("IS")
        temp = self.Expression()
        self.rot = temp.GetValue()
        self.back("RotStatement")

    def ForStatement(self):     # for-draw语句
        self.enter("ForStatement")
        start = 0.0
        end = 0.0
        step = 0.0
        self.MatchToken(TokenType.FOR)
        self.call_match("FOR")
        self.MatchToken(TokenType.T)
        self.call_match("T")
        self.MatchToken(TokenType.FROM)
        self.call_match("FROM")
        start_ptr = self.Expression()
        start = start_ptr.GetValue()
        self.MatchToken(TokenType.TO)
        self.call_match("TO")
        end_ptr = self.Expression()
        end = end_ptr.GetValue()
        self.MatchToken(TokenType.STEP)
        self.call_match("STEP")
        step_ptr = self.Expression()
        step = step_ptr.GetValue()
        self.Tvalue = np.arange(start, end, step)
        self.MatchToken(TokenType.DRAW)
        self.call_match("DRAW")
        self.MatchToken(TokenType.L_BRACKET)
        self.call_match("(")
        self.x_ptr = self.Expression()
        self.x_ptr = self.x_ptr.value
        self.MatchToken(TokenType.COMMA)
        self.call_match(",")
        self.y_ptr = self.Expression()
        self.y_ptr = self.y_ptr.value
        self.MatchToken(TokenType.R_BRACKET)
        self.call_match(")")
        self.back("ForStatement")

    def Expression(self):   # 识别由正负号或无符号开头，以加减号连接的语法
        self.enter("Expression")
        left = self.Term()
        while self.token.type == TokenType.PLUS or self.token.type == TokenType.MINUS:
            temp = self.token.type
            self.MatchToken(temp)
            right = self.Term()
            left = self.GeneratNode(temp, left, right)
        self.ShowTree(left)
        self.back("Expression")
        return left
    
    def Term(self):         # 识别以乘除号连接的语法
        left = self.Factor()
        while self.token.type == TokenType.MUL or self.token.type == TokenType.DIV:
            temp = self.token.type
            self.MatchToken(temp)
            right = self.Factor()
            left = self.GeneratNode(temp, left, right)
        return left
    
    def Factor(self):       # 识别一个标识符或数字、或括号内
        if self.token.type == TokenType.PLUS:
            self.MatchToken(TokenType.PLUS)
            right = self.Factor()
            left = None
            right = self.GeneratNode(TokenType.PLUS, left, right)
        elif self.token.type == TokenType.MINUS:
            self.MatchToken(TokenType.MINUS)
            right = self.Factor()
            left = ExprNode(TokenType.CONST_ID)
            left.value = 0.0
            right = self.GeneratNode(TokenType.MINUS, left, right)
        else:
            right = self.Component()
        return right
    
    def Component(self):    # 识别幂次
        left = self.Atom()
        if self.token.type == TokenType.POWER:
            self.MatchToken(TokenType.POWER)
            right = self.Component()
            left = self.GeneratNode(TokenType.POWER, left, right)
        return left
    
    def Atom(self):         # 识别函数、常数、参数
        if self.token.type == TokenType.CONST_ID:
            temp = self.token.value
            self.MatchToken(TokenType.CONST_ID)
            address = self.GeneratNode_CONST(TokenType.CONST_ID, temp)
        elif self.token.type == TokenType.T:
            self.MatchToken(TokenType.T)
            if len(self.Tvalue) == 1:
                address = self.GeneratNode_CONST(TokenType.T, 0.0)
            else:
                address = self.GeneratNode_CONST(TokenType.T, self.Tvalue)
        elif self.token.type == TokenType.FUNC:
            temp_ptr = self.token.funcptr
            self.MatchToken(TokenType.FUNC)
            self.MatchToken(TokenType.L_BRACKET)
            self.call_match("(")
            temp = self.Expression()
            address = self.GeneratNode(TokenType.FUNC, temp_ptr, temp)
            self.MatchToken(TokenType.R_BRACKET)
            self.call_match(")")
        elif self.token.type == TokenType.L_BRACKET:
            self.MatchToken(TokenType.L_BRACKET)
            self.call_match("(")
            address = self.Expression()
            self.MatchToken(TokenType.R_BRACKET)
            self.call_match(")")
        else:
            self.log(f"{self.token.type}")
            self.log(f"ERROR in line {self.scanner.line_num}, Error Mark: {self.token.lexeme}")
            # sys.exit(1)
        return address
    
    def GeneratNode(self, item, left, right):  # 生成节点
        ExprPtr = ExprNode(item)
        if item == TokenType.FUNC:
            ExprPtr.funcptr = left
            ExprPtr.middle = right
        else:
            ExprPtr.left = left
            ExprPtr.right = right
        ExprPtr.GetValue()                      # 更新Value
        return ExprPtr
    
    def GeneratNode_CONST(self, item, value):  # 常数和变量的节点，叶子结点
        ExprPtr = ExprNode(item)
        ExprPtr.value = value
        return ExprPtr
    
    def GeneratNode_CONST_COL(self, item, color):
        ExprPtr = ExprNode(item)
        ExprPtr.value = color
        return ExprPtr

    def log(self, message, newline=True):
        if newline:
            self.ParserOutput += f"{message}\n"
        else:
            self.ParserOutput += message


    def GetLog(self):
        return self.ParserOutput