from flask import Flask, redirect, url_for, render_template
from livereload import Server

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("registration.html")

@app.route("/paper")
def paper():
    return render_template("paper.html")

if __name__ == "__main__":
    app.debug = True

    # Use livereload server instead of app.run
    server = Server(app.wsgi_app)
    # Watch for changes in templates and static files
    server.watch('templates/')
    server.watch('static/')
    # Start the livereload server
    server.serve(port=5000)