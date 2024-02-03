from flask import Flask, render_template, request, redirect, url_for, flash, session
from DB_handle import DBModule

app = Flask("BulletinBoard")
app.secret_key = "Bulletin_Board_Skey"
DB = DBModule()

@app.route("/")
def home():
    u_data = []
    if "user_id" in session:
        user = session["user_id"]
        u_data = DB.get_userdata(user)
    else:
        user = "False"
    return render_template("home.html", user=user, u_data=u_data)

@app.route("/board")
def board():
    return render_template("board.html")

@app.route("/logout")
def logout():
    if "user_id" in session:
        session.pop("user_id")
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

@app.route("/login")
def login():
    if "user_id" in session:
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/login_action", methods=["get"])
def login_action():
    user_id = request.args.get("id")
    user_password = request.args.get("password")
    if DB.login_verification(user_id, user_password) == 1:
        session["user_id"] = user_id
        return redirect(url_for("home"))
    elif DB.login_verification(user_id, user_password) == 0:
        flash("비밀번호가 틀립니다.")
        return redirect(url_for("login"))
    else:
        flash("존재하지 않는 아이디입니다.")
        return redirect(url_for("login"))

@app.route("/register")
def register():
    if "user_id" in session:
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/register_action", methods=["get"])
def register_action():
    user_id = request.args.get("id")
    user_passward = request.args.get("password")
    user_name = request.args.get("name")
    user_email = request.args.get("email")
    if DB.register(user_id, user_passward, user_name, user_email):
        session["user_id"] = user_id
        return redirect(url_for("home"))
    else:
        flash("이미 존재하는 아이디 입니다.")
        return redirect(url_for("register"))

app.run("127.0.0.1", debug=True)