# SIMPLE_DRAWING_INTERPRETER
简单的绘图语言解释器 by sky

## 环境要求
1. Python      3.12.4
2. matplotlib  3.8.4
3. Flask       3.0.3(可选)

## 使用方法
如果没有安装Flask框架修改`Main.py`中的`scanner = Scanner(test_str2)`将输入语句以字符串形式传入词法分析器，运行后输出在`./static/output.png`。

如果安装了Flask框架可以运行`app.py`（chatgpt常用的Flask框架文件名），在网页端进行输入与显示操作。

需要注意的是两者共享同一个输出目录，可能存在相互覆盖等问题，注意保存输出文件。

## 项目结构
见[我的博客](https://skyjty.github.io/notes/2025/01/13/Simple_drawing_interpreter.html)

## License
This code is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/) for non-commercial use only.
Please note that any commercial use of this code requires formal permission prior to use.

## 感谢
感谢编译原理教师王老师的教学，感谢前辈[BBBBchan](https://github.com/BBBBchan)提供的参考文档，代码文件与开源许可。