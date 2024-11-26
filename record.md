## 0 前言
### 0.1 简述
`编译原理`课程要求完成一个简单的绘图语言解释器，笔者准备完成一个基于`Python`及其`flask`框架的解释器，顺便复习知识点以及完善编译原理笔记。

### 0.2 要求
为函数绘图语言编写一个解释器，输入为用函数绘图语言编写的源程序
1. 用词法分析器识别其中的记号（可将记号的信息显示出来）；
2. 用语法分析器识别记号流中的语句（可将语句结构显示出来）；
3. 解释器：词法分析、语法分析、语义分析/计算，绘制图形。

### 0.3 函数绘图语言
举例：
```py
-------------------------- 函数f(t)=t的图形
origin is (100, 300);	-- 设置原点的偏移量
rot is 0;			    -- 设置旋转角度(不旋转)
scale is (1, 1);		-- 设置横坐标和纵坐标的比例
for T from 0 to 200 step 1 draw (t, 0);
                        -- 横坐标的轨迹（纵坐标为0）
for T from 0 to 150 step 1 draw (0, -t);
                        -- 纵坐标的轨迹（横坐标为0）
for T from 0 to 120 step 1 draw (t, -t);
                        -- 函数f(t)=t的轨迹 
```

语句满足下述规定(原则)：
1. 各类语句可以按任意次序书写，且非注释语句以分号结尾。解释器按照语句出现的先后顺序处理。 
2. `ORIGIN` 、`ROT` 和 `SCALE` 语句只影响其后的绘图语句，且遵循最后出现的语句有效的原则。
    例如，若有下述`ROT`语句序列：
    ```python
    ROT IS 0.7 ；  …
    ROT IS 1.57 ； …
    ```
    则随后的绘图语句将按1.57而不是0.7弧度旋转。 
3. 无论`ORIGIN` 、`ROT` 和`SCALE` 语句的出现顺序如何，图形的变换顺序总是：比例变换→旋转变换→平移变换 
4. 语言对大小写不敏感，例如`for` 、`For` 、`FOR` 等，均被认为是同一个保留字。 （处理时将所有字母大写）
5. 语句中表达式的值均为双精度类型，旋转角度单位为弧度且为逆时针旋转，平移单位为像素点。  

## 1 词法分析器(scanner)
词法分析器确定输入的每个记号的正确与否，包括常数、参数、函数、保留字、运算符、分隔符。
词法分析器需要将标记记号的种类，供语法分析器使用；去除无用部分如空格，回车等；发生错误时报错。

### 1.1 Token类
Token类负责初始化并保存每个记号的相关数据。
ppt提供的数据结构：
```c
struct Token
{	enum Token_Type  type;      // 类别，见下页
    char * lexeme;              // 属性，原始输入的字符串，亦可为数组
    double value;               // 属性，若记号是常数则存常数的值
    double (* FuncPtr)(double); // 属性，若记号是函数则存函数地址
    // … 按需增加其他成员 …
}; 

enum Token_Type	                // 记号的类别
{
    ID,  COMMENT,               // 参见正规式设计
    ORIGIN, SCALE, ROT, IS,     // 保留字（一字一码）
    TO, STEP, DRAW,FOR, FROM,   // 保留字
    T,                          // 参数
    SEMICO, L_BRACKET, R_BRACKET, COMMA,// 分隔符
    PLUS, MINUS, MUL, DIV, POWER,		// 运算符
    FUNC,                       // 函数（调用）
    CONST_ID,                   // 常数
    NONTOKEN,                   // 空记号（源程序结束）
    ERRTOKEN                    // 出错记号（非法输入）
}; 

struct Token TokenTab[] =
{
    {CONST_ID,	"PI",		3.1415926,	NULL},
    {CONST_ID,	"E",		2.71828,	NULL},
    {T,		    "T",		0.0,		NULL},
    {FUNC,		"SIN",		0.0,		sin},
    {FUNC,		"COS",		0.0,		cos},
    {FUNC,		"TAN",		0.0,		tan},
    {FUNC,		"LN",		0.0,		log},
    {FUNC,		"EXP",		0.0,		exp},
    {FUNC,		"SQRT",		0.0,		sqrt},
    {ORIGIN,	"ORIGIN",	0.0,		NULL},
    {SCALE,		"SCALE",	0.0,		NULL},
    {ROT,		"ROT",		0.0,		NULL},
    {IS,		"IS",		0.0,		NULL},
    {FOR,		"FOR",		0.0,		NULL},
    {FROM,		"FROM",		0.0,		NULL},
    {TO,		"TO",		0.0,		NULL},
    {STEP,		"STEP",		0.0,		NULL},
    {DRAW,		"DRAW",		0.0,		NULL}
};
```
修改为python语句：
```py
from enum import Enum
import numpy as np

Token_Type = Enum("Token_Type", (
    "ID", "COMMENT",                                # 参见正规式设计
    "ORIGIN", "SCALE", "ROT", "IS",                 # 保留字（一字一码）
    "TO", "STEP", "DRAW", "FOR", "FROM",            # 保留字
    "T",                                            # 参数
    "SEMICO", "L_BRACKET", "R_BRACKET", "COMMA",    # 分隔符
    "PLUS", "MINUS", "MUL", "DIV", "POWER",         # 运算符
    "FUNC",                                         # 函数（调用）
    "CONST_ID",                                     # 常数
    "NONTOKEN",                                     # 空记号（源程序结束）
    "ERRTOKEN"                                      # 出错记号（非法输入）
))


class Tokens:
    def __init__(self, type, lexeme, value, funcptr):
        self.lexeme = lexeme    # 字符串属性
        self.value = value      # 常数值属性
        self.funcptr = funcptr  # 函数指针
        if type in Token_Type:
            self.type = type    # token类别
        else:
            print("invalid token")

TokenTab = {
    "PI": Tokens(Token_Type.CONST_ID, "PI", 3.1415926, None),
    "E": Tokens(Token_Type.CONST_ID, "E", 2.71828, None),
    "T": Tokens(Token_Type.T, "T", 0.0, None),
    "SIN": Tokens(Token_Type.FUNC, "SIN", 0.0, np.sin),
    "COS": Tokens(Token_Type.FUNC, "COS", 0.0, np.cos),
    "TAN": Tokens(Token_Type.FUNC, "TAN", 0.0, np.tan),
    "LN": Tokens(Token_Type.FUNC, "LN", 0.0, np.log),
    "EXP": Tokens(Token_Type.FUNC, "EXP", 0.0, np.exp),
    "SQRT": Tokens(Token_Type.FUNC, "SQRT", 0.0, np.sqrt),
    "ORIGIN": Tokens(Token_Type.ORIGIN, "ORIGIN", 0.0, None),
    "SCALE": Tokens(Token_Type.SCALE, "SCALE", 0.0, None),
    "ROT": Tokens(Token_Type.ROT, "ROT", 0.0, None),
    "IS": Tokens(Token_Type.IS, "IS", 0.0, None),
    "FOR": Tokens(Token_Type.FOR, "FOR", 0.0, None),
    "FROM": Tokens(Token_Type.FROM, "FROM", 0.0, None),
    "TO": Tokens(Token_Type.TO, "TO", 0.0, None),
    "STEP": Tokens(Token_Type.STEP, "STEP", 0.0, None),
    "DRAW": Tokens(Token_Type.DRAW, "DRAW", 0.0, None)
}
```

### 1.2 Scanner类
Scanner类负责将符号保存到Token类中并处理异常情况。
课程示例中该类的输入为文件名，笔者想要基于Flask框架完成一个界面来展示，该处输入应该为代码的字符串。为方便编写，笔者查询到了`StringIO`类，该类允许用户将`String`类看作一个文件进行读写操作。

具体代码见项目，此处笔者根据参照内容将多个函数简化为判断语句。

## 2 语法分析器(parser)
语法分析器的主要工作如下：
1. 设计函数绘图语言的文法，使其适合递归下降分析；
2. 设计语法树的结构，用于存放表达式的语法树；
3. 设计递归下降子程序，分析句子并构造表达式的语法树；
4. 设计测试程序和测试用例，检验分析器是否正确。

在ppt中提供了使用文法的具体推导过程，(to be record)

最终文法如下：
```js
Program         →   { Statement SEMICO } 
Statement       →   OriginStatment | ScaleStatment
                    | RotStatment  | ForStatment
OriginStatment  →   ORIGIN IS 
                    L_BRACKET Expression COMMA Expression R_BRACKET
ScaleStatment   →   SCALE IS 
                    L_BRACKET Expression COMMA Expression R_BRACKET
RotStatment     →   ROT IS Expression

Expression      →   Term { ( PLUS | MINUS ) Term } 
Term            →   Factor { ( MUL | DIV ) Factor }
Factor  	    →   ( PLUS | MINUS ) Factor | Component
Component       →   Atom [ POWER Component ]

Atom            →   CONST_ID
                    | T
                    | FUNC L_BRACKET Expression R_BRACKET
                    | L_BRACKET Expression R_BRACKET 
```
由于这是一个EBNF格式，笔者并未找到课程内的相关解释，此处记录相关符号如下：

|记号|意义|
|--         |--|
|=          |定义（此处被替换为→）|
|,          |连接符（此处被忽略）|
|;(SEMICO)  |结束符|
|&#124;     |或|
|[...]      |可选|
|{...}      |重复|
|(...)      |分组|
|"..."      |终端字符串|
|'...'      |终端字符串|
|(*...*)    |注释|
|?...?      |特殊数列|
|-          |除外|

## 添加内容
### COLOR语句
尝试添加Color声明
先看看color的语句例子：
```py
color is (255,255,0);
```
首先添加TOKEN：
```py
TokenType = Enum("Token_Type", (
    ...
    #ADD BY SKY
    "COLOR"                                         # 颜色设置
))

TokenTab = {
    ...
    #ADD BY SKY
    "COLOR": Tokens(TokenType.COLOR, "COLOR", 0.0, None)
}
```
然后在Scanner_tester中测试：
```js
token_lexeme         token_value  token_value  token_funcptr
------------------------------------------------------------
Token_Type.COLOR    |COLOR       |    0.000000|None
Token_Type.IS       |IS          |    0.000000|None
Token_Type.L_BRACKET|(           |    0.000000|None
Token_Type.CONST_ID |255         |  255.000000|None
Token_Type.COMMA    |,           |    0.000000|None
Token_Type.CONST_ID |255         |  255.000000|None
Token_Type.COMMA    |,           |    0.000000|None
Token_Type.CONST_ID |0           |    0.000000|None
Token_Type.R_BRACKET|)           |    0.000000|None
Token_Type.SEMICO   |;           |    0.000000|None
Token_Type.NONTOKEN |            |    0.000000|None
```
可以正常读取。

为了添加color声明语句，需要修改原先的状态转移图：

```js
Program         →   { Statement SEMICO } 
Statement       →   OriginStatment | ScaleStatment
                    | RotStatment  | ForStatment   | ColorStatment
...

ColorStatment   →   COLOR IS 
                    L_BRACKET Expression COMMA Expression COMMA Expression R_BRACKET
...
```

故需要在Parser_process以及Semantic中修改函数Statment(),添加ColorStatement()声明语句以及相关变量：
```py
class Parser(object):
    def __init__(self,scanner):
        ...
        self.color = [0,0,0]
    ...
    def Statement(self):        # 为每一个语句转进每一种文法
        self.enter("Statement")
        if self.token.type == TokenType.ORIGIN:
        ...
        # ADD BY SKY
        elif self.token.type == TokenType.COLOR:
            self.ColorStatement()
        ...
        self.back("Statement")
    ...
    def ColorStatement(self):   # color语句
        self.enter("ColorStatement")
        self.MatchToken(TokenType.COLOR)
        self.call_match("COLOR")
        self.MatchToken(TokenType.IS)
        self.call_match("IS")
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
        self.back("ColorStatement")
```
再修改Semantic中的Draw函数
```py
def Draw(self):
    x, y = self.calc(self.x_ptr, self.y_ptr)
    color_normalized = [(c % 256) / 255 for c in self.color]
    self.ax.scatter(x, y, color=color_normalized)
```
为了确保正常运行，此处将颜色常量对256取余后作除法，处理不在[0,255]的常量。

#### 颜色常量
还存在BLUE表示蓝色等常量，但该常量与PI等常量不同的是该常量是包含3个值的数组，python由于并不重视类型诸多函数不需要进行修改，但相比于COLOR修改的内容较多。

文法如下：
```js
Program         →   { Statement SEMICO } 
Statement       →   OriginStatment | ScaleStatment
                    | RotStatment  | ForStatment   | ColorStatment
...

ColorStatment   →   COLOR IS ColorExpression
ColorExpression →   L_BRACKET Expression COMMA Expression COMMA Expression R_BRACKET
                →   CONST_COL
...

```

对于Scanner，扫描时token.value的输出log函数需要修改，如果是元组需要将输出修改为字符串，而且由于原value字段长度最长为12，而最长的颜色白色`[255 ,255 ,255]`有15个字符，故将value字段扩展到16位。

```py
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
```

在Parser中token.value的log函数同样需要修改。

```py
def PrintTree(self,root,indent):
    ...
    # 适配颜色常量
    elif root.item == TokenType.CONST_ID:
        if isinstance(root.value, (int, float)):  # 如果是整数或浮点数
            self.log(f"{root.value:.5f}")  # 保留 5 位小数
        elif isinstance(root.value, tuple):  # 如果是元组
            self.log(f"({', '.join(f'{v:.5f}' if isinstance(v, (int, float)) else str(v) for v in root.value)})")
        else:  # 其他类型
            self.log(str(root.value))
    ...
```

Parser的测试结果正常：
```js
...
Enter Statement
Enter ColorStatement
Match Token COLOR
Match Token IS
Enter Expression
        [0, 0, 255]
Leave Expression
Leave ColorStatement
Leave Statement
Match Token ;
...
```


