from Token import *
from io import StringIO

class Scanner:
    def __init__(self,in_str):      #初始化变量，将输入转化为StringIO类
        self.line_num = 0
        self.token_buffer = ''
        self.in_str = in_str
        self.ScannerOutput = ''
        if len(self.in_str) != 0:
            self.s_ptr = StringIO(self.in_str)
        else:
            self.s_ptr = None
            print("Empty Input.")

    def CloseScanner(self):
        if self.s_ptr is None:
            self.s_ptr.close()
    
    def GetChar(self):              #读取一个字符
        char = self.s_ptr.read(1)   #读取字符
        return char.upper()         #返回大写

    def BackChar(self,char):        #回退一个字符
        if char != '':
            self.s_ptr.seek(self.s_ptr.tell() - 1)  #找到指针位置并回退
    
    def AddBuffer(self,char):       #加入缓存
        self.token_buffer += char

    def BackBuffer(self):           #回退缓存
        self.token_buffer = self.token_buffer[:-1]

    def ClearBuffer(self):          #清空缓存
        self.token_buffer = ''

    def ErrorToken(self,str):
        return Tokens(TokenType.ERRTOKEN, str, 0.0, None)

    def IsToken(self):              #判断是否Token
        token = TokenTab.get(self.token_buffer, self.ErrorToken(self.token_buffer))
        return token
    
    def GetToken(self):
        # if self.line_num == 0:
        #     self.line_num = 1
        self.ClearBuffer()
        char = ''
        token = ''
        while True:                 #处理结束符、空格、回车
            char = self.GetChar()
            if char == '':
                token = Tokens(TokenType.NONTOKEN, char, 0.0, None)
                return token
            if char == '\n':
                self.line_num+=1
            if not char.isspace():
                break
        self.AddBuffer(char)        #读取第一个字符

        if char.isalpha():          #字母开始内容
            while True:
                char = self.GetChar()
                if char.isalnum():
                    self.AddBuffer(char)
                else:
                    break
            self.BackChar(char)
            token = self.IsToken()
            token.lexeme = self.token_buffer
            return token
        
        elif char.isdigit():        #数字开始内容
            while True:
                char = self.GetChar()
                if char.isdigit():
                    self.AddBuffer(char)
                else:
                    break
            if char == '.':
                self.AddBuffer(char)
                while True:
                    char = self.GetChar()
                    if char.isdigit():
                        self.AddBuffer(char)
                    else:
                        break

            self.BackChar(char)
            token = Tokens(
                TokenType.CONST_ID, self.token_buffer, float(self.token_buffer), None
                )
            return token
        
        elif char == '.':
            self.BackBuffer()
            self.AddBuffer('0'+char)
            while True:
                char = self.GetChar()
                if char.isdigit():
                    self.AddBuffer(char)
                else:
                    break
            self.BackChar(char)
            token = Tokens(
                TokenType.CONST_ID, self.token_buffer, float(self.token_buffer), None
                )
            return token
        
        else:                       #注释，括号，运算符，结束符
            if char == ';':
                token = Tokens(TokenType.SEMICO, char, 0.0, None)
            elif char == '(':
                token = Tokens(TokenType.L_BRACKET, char, 0.0, None)
            elif char == ')':
                token = Tokens(TokenType.R_BRACKET, char, 0.0, None)
            elif char == ',':
                token = Tokens(TokenType.COMMA, char, 0.0, None)
            elif char == '+':
                token = Tokens(TokenType.PLUS, char, 0.0, None)
            elif char == '-':
                char = self.GetChar()
                if char == '-':
                    while char != '\n' and char != '':
                        char = self.GetChar()
                    self.BackChar(char)
                    return self.GetToken()
                else:
                    self.BackChar(char)
                    token = Tokens(TokenType.MINUS, char, 0.0, None)
            elif char == '/':
                char = self.GetChar()
                if char == '/':
                    while char != '\n' and char != '':
                        char = self.GetChar()
                    self.BackChar(char)
                    return self.GetToken()
                else:
                    self.BackChar(char)
                    token = Tokens(TokenType.DIV, char, 0.0, None)
            elif char == '*':
                char = self.GetChar()
                if char == '*':
                    token = Tokens(TokenType.POWER, char, 0.0, None)
                else:
                    self.BackChar(char)
                    token = Tokens(TokenType.MUL, char, 0.0, None)
            elif char == '\n' or char == '':
                return self.GetToken()
            else:
                token = self.ErrorToken(char)
        return token

    def log(self, message, newline=True):
        """
        Logs a message to ParserOutput. Appends a newline by default.
        :param message: The message to log.
        :param newline: Whether to add a newline after the message.
        """
        if newline:
            self.ScannerOutput += f"{message}\n"
        else:
            self.ScannerOutput += message

    def LogToken(self,token,width_value=16):
        if isinstance(token.value, tuple):  # 如果是元组，转成字符串
            value_str = str(token.value).rjust(width_value)
        elif isinstance(token.value, (int, float)):  # 如果是数值，格式化为浮点数
            value_str = "{:16f}".format(token.value)
        else:  # 其他类型直接转字符串
            value_str = str(token.value).rjust(width_value)

        # 使用格式化后的值输出日志
        self.log("{:20s}|{:12s}|{:16s}|{}".format(
            token.type,  # 类型
            token.lexeme,  # 词素
            value_str,  # 处理后的值
            token.funcptr  # 函数指针
        ))

    def GetLog(self):
        self.log('token_lexeme         token_value   token_value     token_funcptr')
        self.log('----------------------------------------------------------------')
        current_pos = self.s_ptr.tell()
        while True:
            token = self.GetToken()
            if token.type != TokenType.NONTOKEN:
                self.LogToken(token)  # 调用自定义方法来处理打印每个token
            else:
                self.LogToken(token)
                break

        self.s_ptr.seek(current_pos)  #恢复开始读取位置
        
        self.log("")  # 添加空行
        self.log(f"{self.line_num} lines in all.")  # 输出总行数
        return self.ScannerOutput