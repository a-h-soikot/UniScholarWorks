from flask import Flask, redirect, url_for, render_template, session, request, flash, send_from_directory, abort
import os
import database_queries as db_queries

from datetime import timedelta
from livereload import Server

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a secure random key for session management
app.permanent_session_lifetime = timedelta(days=1)  # Set session lifetime



@app.route("/login", methods=["GET", "POST"])
def login():
    
    if "user_id" in session:
        return redirect(url_for("home"))
    
    # Check if this is a form submission
    if request.method == "POST":
        user_id = request.form.get("userid")
        password = request.form.get("password")
        
        # Validate the credentials
        user = db_queries.get_user_by_credentials(user_id, password)
        
        if user:
            # Store user info in session
            session["user_id"] = user.get_user_id()
            session["email"] = user.get_email()
            session["name"] = user.get_name()
            
            session.permanent = True
            # Redirect to home page after successful login
            return redirect(url_for("home"))
        else:
            # Show error message for failed login
            error = "Invalid username or password"
            return render_template("login.html", error=error)
            
    # For GET requests, just show the login form
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("registration.html")

@app.route("/logout")
def logout():
    # Clear the session data
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    reports = db_queries.get_reports() 
    return render_template("home.html", reports=reports)


@app.route("/report/<int:report_id>")
def report(report_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    report = db_queries.get_report_by_id(report_id)
    return render_template("report.html", report=report)

@app.route("/report_review")
def report_review():
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    return render_template("report_review.html")


@app.route("/download/<file_id>")
def download_file(file_id):
    # Check if user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))
        
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