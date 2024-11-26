from enum import Enum
import numpy as np

TokenType = Enum("Token_Type", (
    "ID", "COMMENT",                                # 参见正规式设计
    "ORIGIN", "SCALE", "ROT", "IS",                 # 保留字（一字一码）
    "TO", "STEP", "DRAW", "FOR", "FROM",            # 保留字
    "T",                                            # 参数
    "SEMICO", "L_BRACKET", "R_BRACKET", "COMMA",    # 分隔符
    "PLUS", "MINUS", "MUL", "DIV", "POWER",         # 运算符
    "FUNC",                                         # 函数（调用）
    "CONST_ID",                                     # 常数
    "NONTOKEN",                                     # 空记号（源程序结束）
    "ERRTOKEN",                                     # 出错记号（非法输入）
    #ADD BY SKY
    "COLOR",                                        # 颜色设置
    "CONST_COL"                                     # 颜色常量
))


class Tokens:
    def __init__(self, type, lexeme, value, funcptr):
        self.lexeme = lexeme    # 字符串属性
        self.value = value      # 常数值属性
        self.funcptr = funcptr  # 函数指针
        if type in TokenType:
            self.type = type    # token类别
        else:
            print("invalid token")

TokenTab = {
    "PI": Tokens(TokenType.CONST_ID, "PI", 3.1415926, None),
    "E": Tokens(TokenType.CONST_ID, "E", 2.71828, None),
    "T": Tokens(TokenType.T, "T", 0.0, None),
    "SIN": Tokens(TokenType.FUNC, "SIN", 0.0, np.sin),
    "COS": Tokens(TokenType.FUNC, "COS", 0.0, np.cos),
    "TAN": Tokens(TokenType.FUNC, "TAN", 0.0, np.tan),
    "LN": Tokens(TokenType.FUNC, "LN", 0.0, np.log),
    "EXP": Tokens(TokenType.FUNC, "EXP", 0.0, np.exp),
    "SQRT": Tokens(TokenType.FUNC, "SQRT", 0.0, np.sqrt),
    "ORIGIN": Tokens(TokenType.ORIGIN, "ORIGIN", 0.0, None),
    "SCALE": Tokens(TokenType.SCALE, "SCALE", 0.0, None),
    "ROT": Tokens(TokenType.ROT, "ROT", 0.0, None),
    "IS": Tokens(TokenType.IS, "IS", 0.0, None),
    "FOR": Tokens(TokenType.FOR, "FOR", 0.0, None),
    "FROM": Tokens(TokenType.FROM, "FROM", 0.0, None),
    "TO": Tokens(TokenType.TO, "TO", 0.0, None),
    "STEP": Tokens(TokenType.STEP, "STEP", 0.0, None),
    "DRAW": Tokens(TokenType.DRAW, "DRAW", 0.0, None),
    #ADD BY SKY
    "COLOR": Tokens(TokenType.COLOR, "COLOR", 0.0, None),
    "BLUE": Tokens(TokenType.CONST_COL, "BLUE", [0,0,255], None),
    "GREEN": Tokens(TokenType.CONST_COL, "GREEN", [0,255,0], None),
    "RED": Tokens(TokenType.CONST_COL, "RED", [255,0,0], None),
    "BLACK": Tokens(TokenType.CONST_COL, "BLACK", [0,0,0], None),
    "WHITE": Tokens(TokenType.CONST_COL, "WHITE", [255,255,255], None)
}
