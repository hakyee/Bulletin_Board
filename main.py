from flask import Flask, render_template, request, redirect

app = Flask("BulletinBoard")

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

app.run("127.0.0.1", debug=True)