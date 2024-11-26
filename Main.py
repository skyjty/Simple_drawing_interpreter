import Scanner
from Semantic import *
from Scanner import *
from Token import *

my_str = '''
rot is 0;
origin is (0, 0);
scale is (2,20);
for T from 1 to 300 step 1 draw (t,-ln(t));
scale is (20,0.1);
for T from 0 to 8 step 0.1 draw (t,exp(t));
scale is (2,1);
for T from 0 to 300 step 1 draw (t,0);
for T from 0 to 300 step 1 draw (0,t);
for T from 0 to 120 step 1 draw (t,t);
scale is (2,0.1);
for T from 0 to 55 step 1 draw (t,-(t*t));
scale is (10,5);
for T from 0 to 60 step 1 draw (t,sqrt(t));
'''

exp_str = '''
rot is 0;
origin is (0, 0);
scale is (20,0.1);
for T from 0 to 8 step 0.1 draw (t,exp(t));
'''

test_str = '''
rot is 0;
origin is (0, 0);
scale is (2,20);
for T from 1 to 300 step 1 draw (t,-ln(t));
scale is (20,0.1);
for T from 0 to 8 step 0.1 draw (t,exp(t));
scale is (2,1);
for T from 0 to 300 step 1 draw (t,0);
for T from 0 to 300 step 1 draw (0,t);
for T from 0 to 120 step 1 draw (t,t);
scale is (2,0.1);
for T from 0 to 55 step 1 draw (t,-(t*t));
scale is (10,5);
for T from 0 to 60 step 1 draw (t,sqrt(t));
'''

heart_str = '''
rot is -pi/2;
origin is (0, 0);
color is (255,0,0);
for t from -pi to pi step pi/200 draw((2*cos(t) - cos(2*t)),  (2*sin(t)-sin(2*t))  );
'''

test_str2 = '''------- 函数f(t)=t的图形
origin is (0, 0);	-- 设置原点的偏移量
scale is (2, 1);	-- 设置横、纵坐标缩放比例
rot is pi/2;		-- 设置旋转角度
for T from 0 to 200 step 1 draw (t, 0);	-- 横坐标
for T from 0 to 180 step 1 draw (0, t);	-- 纵坐标
for T from 0 to 150 step 1 draw (t, t);	-- f(t)=t
'''

scanner = Scanner(heart_str)
print(scanner.GetLog())

semantic = Semantic(scanner)

semantic.init()
semantic.Parser()

save_path = "./static/test.png"
semantic.SaveFig(save_path)

print(semantic.GetLog())