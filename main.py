from flask import Flask, render_template, request, redirect, url_for, flash
from DB_handle import DBModule

app = Flask("BulletinBoard")
app.secret_key = "Bulletin_Board_Skey"
DB = DBModule()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/board")
def board():
    return render_template("board.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register_action", methods=["get"])
def register_action():
    user_id = request.args.get("id")
    user_passward = request.args.get("password")
    user_name = request.args.get("name")
    user_email = request.args.get("email")
    if DB.register(user_id, user_passward, user_name, user_email):
        return redirect(url_for("home"))
    else:
        flash("이미 존재하는 아이디 입니다.")
        return redirect(url_for("register"))

app.run("127.0.0.1", debug=True)