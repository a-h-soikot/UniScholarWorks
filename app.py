from flask import Flask, redirect, url_for, render_template
import database_queries as db_queries

from livereload import Server

app = Flask(__name__)


@app.route("/")
def home():
    reports = db_queries.get_reports() 
    return render_template("home.html", reports=reports)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("registration.html")

@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/report_review")
def report_review():
    return render_template("report_review.html")

if __name__ == "__main__":
    app.debug = True

    # Use livereload server instead of app.run
    server = Server(app.wsgi_app)
    # Watch for changes in templates and static files
    server.watch('templates/')
    server.watch('static/')
    # Start the livereload server
    server.serve(port=5000)