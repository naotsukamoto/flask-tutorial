#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template,request,session,redirect,url_for
# OnegaiContentクラスをimport
from models.models import OnegaiContent
# Userクラスをimport
from models.models import User
# add()を実行するために、db_session をimport、データベースに時間を追加するのでdatetimeをインポート
from models.database import db_session
from datetime import datetime
# SALT利用のため
from app import config
# ハッシュ化のため
from hashlib import sha256


#Flaskオブジェクトの生成
app = Flask(__name__)
# セッション情報の暗号化
app.secret_key = config.SECRET_KEY

@app.route("/")

@app.route("/index")
def index():
    if "user_name" in session:
        name = session["user_name"]
        all_onegai = OnegaiContent.query.all()
        return render_template("index.html",name=name,all_onegai=all_onegai)
    else:
        return redirect(url_for("top",status="logout"))

@app.route("/index", methods=["post"])
def post():
    name = request.form["name"]
    all_onegai = OnegaiContent.query.all()
    return render_template("index.html",name=name,all_onegai=all_onegai)

@app.route("/add",methods=["post"])
def add():
    title = request.form["title"]
    body = request.form["body"]
    content = OnegaiContent(title,body,datetime.now())
    db_session.add(content)
    db_session.commit()
    return redirect(url_for("index"))

@app.route("/update",methods=["post"])
def update():
    content = OnegaiContent.query.filter_by(id=request.form["update"]).first()
    content.title = request.form["title"]
    content.body = request.form["body"]
    db_session.add(content)
    db_session.commit()
    return redirect(url_for("index"))

@app.route("/delete",methods=["post"])
def delete():
    id_list = request.form.getlist("delete")
    # debug
    print(request.form)
    for id in id_list:
        content = OnegaiContent.query.filter_by(id=id).first()
        db_session.delete(content)
    db_session.commit()
    return redirect(url_for("index"))

@app.route("/top")
def top():
    status = request.args.get("status")
    return render_template("top.html",status=status)

@app.route("/newcomer")
def new():
    status = request.args.get("status")
    return render_template("newcomer.html",status=status)

# ログイン処理
@app.route("/login",methods=["post"])
def login():
    # ログインフォームに入力したusernameを取得
    user_name = request.form["user"]
    # 対象のusernameのレコードを抽出
    user = User.query.filter_by(user_name=user_name).first()
    if user:
    # 対象のusernameのレコードが存在すれば、次にパスワードの確認に進む
        password = request.form["password"]
        hashed_password = sha256((user_name + password + config.SALT).encode("utf-8")).hexdigest()
        if user.hashed_password == hashed_password:
            # ハッシュ化したパスワード同士が一致すれば、セッションをcookieに記録して/index にリダイレクト
            session["user_name"] = user_name
            return redirect(url_for("index"))
        else:
            # ハッシュ化したパスワード同士が一致しなれば、パスワードが間違っていることを伝える
            return redirect(url_for("top",status="wrong_password"))
    else:
        # 対象のusernameのレコードが存在しなければ、ユーザーが見つからない旨を返す
        return redirect(url_for("top",status="user_notfound"))

# 登録処理
@app.route("/register",methods=["post"])
def register():
    # ５行目まではログイン処理と同じです。
    user_name = request.form["user"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        return render_template("newcomer.html",status="exist_user")
    else:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + config.SALT).encode("utf-8")).hexdigest()
        new_user = User(user_name,hashed_password)
        db_session.add(new_user)
        db_session.commit()
        session["user_name"] = user_name
        return redirect(url_for("index"))

# ログアウト処理
@app.route("/logout")
def logout():
    session.pop("user_name",None)
    return redirect(url_for("top",status="logout"))

# おまじない
if __name__ == "__main__":
    app.run(debug=True)