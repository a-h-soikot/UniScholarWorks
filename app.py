from flask import Flask, redirect, url_for, render_template, send_from_directory, abort
import os
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

@app.route("/report/<int:report_id>")
def report(report_id):
    report = db_queries.get_report_by_id(report_id)
    return render_template("report.html", report=report)

@app.route("/report_review")
def report_review():
    return render_template("report_review.html")


@app.route("/download/<file_id>")
def download_file(file_id):
    directory = "/home/soikot/Documents/files"
    return send_from_directory(directory, file_id, as_attachment=True)


if __name__ == "__main__":
    app.debug = True

    # Use livereload server instead of app.run
    server = Server(app.wsgi_app)
    # Watch for changes in templates and static files
    server.watch('templates/')
    server.watch('static/')
    # Start the livereload server
    server.serve(port=5000)