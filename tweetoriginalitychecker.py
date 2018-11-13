import os
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("welcome.html")

@app.route('/login')
def login():
    return render_template("auth/login.html")

@app.route('/register')
def register():
    return render_template("auth/register.html")

@app.route('/logout')
def logout():
    return 0

if __name__ == '__main__':
    app.run(debug=True)
