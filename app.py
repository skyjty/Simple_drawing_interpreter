from flask import Flask, render_template, request, send_file
from Scanner import *
from Semantic import *
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    lexer_output = ""
    parser_output = ""
    img_path = None

    if request.method == "POST":
        # 获取用户输入
        user_input = request.form["code"]

        try:
            # 词法分析
            scanner = Scanner(user_input)
            lexer_output = scanner.GetLog()

            # 语义分析和绘图
            semantic = Semantic(scanner)
            semantic.init()
            semantic.Parser()

            parser_output = semantic.GetLog()

            # 保存绘图结果为图片
            img_path = "./static/output.png"
            semantic.SaveFig(img_path)
        except Exception as e:
            lexer_output = scanner.GetLog() + str(e)
            # print(e)

    return render_template(
        "index.html",
        # user_input=user_input,
        lexer_output=lexer_output,
        parser_output=parser_output,
        img_path=img_path,
    )

@app.route("/image")
def get_image():
    return send_file("static/output.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
