from flask import Flask, render_template, request, redirect, url_for, flash, session
from DB_handle import DBModule
import time

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
    p_data = DB.get_postdata()
    if p_data == None:
        p_count = 0
    else:
        p_data = sorted(p_data.items(), key=lambda x: x[1]["write_time"], reverse=True)
        p_count = len(p_data)
    if "user_id" in session:
        user = session["user_id"]
    else:
        user = "False"
    return render_template("board.html", user=user, p_data=p_data, p_count=p_count)

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
    
@app.route("/write")
def write():
    u_data = []
    if "user_id" in session:
        user = session["user_id"]
        u_data = DB.get_userdata(user)
        return render_template("write.html", user=user, u_data=u_data)
    else:
        return redirect(url_for("login"))

@app.route("/write_action", methods=["get"])
def write_action():
    title = request.args.get("title")
    contents = request.args.get("contents")
    write_time = time.strftime('%Y-%m-%d %H:%M:%S')
    user = session["user_id"]
    DB.write(user, title, contents, write_time)
    return redirect(url_for("board"))

@app.route("/view/<string:post_id>")
def view(post_id):
    if "user_id" in session:
        user = session["user_id"]
    else:
        user = "False"
    post_detail = DB.get_post_detail(post_id)
    return render_template("view.html", user=user, p_detail=post_detail)

app.run("127.0.0.1", debug=True)