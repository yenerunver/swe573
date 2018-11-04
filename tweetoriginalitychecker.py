from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Welcome to the application page of Tweet Originality Checker!\n\nHoşgeldiniz!"
