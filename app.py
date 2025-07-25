from flask import Flask, redirect, url_for, render_template, session, request, flash, send_from_directory, abort
import os
import database_queries as db_queries

from datetime import timedelta
from livereload import Server

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a secure random key for session management
app.permanent_session_lifetime = timedelta(days=1)  # Set session lifetime
app.config['SESSION_USE_SIGNER'] = True  # Sign session cookies for security
app.config['SESSION_PERMANENT'] = True   # Make sessions permanent by default
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True  # Preserve context (including flash messages) on exceptions



@app.route("/login", methods=["GET", "POST"])
def login():
    
    if "user_id" in session:
        return redirect(url_for("home"))
    
    # Check if this is a form submission
    if request.method == "POST":
        user_id = request.form.get("userid")
        password = request.form.get("password")

        # Validate the credentials
        user = db_queries.get_user_by_credentials(user_id, password, request.form.get("user_type"))
        
        if user:
            # Store user info in session
            session["user_id"] = user.get_user_id()
            session["email"] = user.get_email()
            session["name"] = user.get_name()
            session["user_type"] = request.form.get("user_type")
            
            session.permanent = True
            # Redirect to home page after successful login
            return redirect(url_for("home"))
        else:
            # Show error message for failed login
            error = "Invalid username or password"
            return render_template("login.html", error=error, user_type=request.form.get("user_type"))
            
    # For GET requests, just show the login form
    user_type = request.args.get("user_type", "student")  # Default to student if not specified
    return render_template("login.html", user_type=user_type)


@app.route("/register")
def register():
    return render_template("registration.html")


@app.route("/logout")
def logout():
    # Clear the session data
    session.clear()
    return redirect(url_for("login"))


@app.route("/", methods=["GET"])
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # Get filter parameters from request
    report_types = request.args.getlist('type')
    tags = request.args.getlist('tag')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Get reports with filters
    reports = db_queries.get_filtered_reports(
        report_types=report_types, 
        tags=tags,
        start_date=start_date,
        end_date=end_date
    )
    
    # Pass both reports and filter selections back to the template
    return render_template("home.html", 
        reports=reports,
        selected_types=report_types,
        selected_tags=tags,
        start_date=start_date,
        end_date=end_date,
        user_type = session["user_type"]
    )


@app.route("/search", methods=["GET"])
def search():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # Get search query
    query = request.args.get('q', '')
    
    if not query:
        return redirect(url_for('home'), user_type = session["user_type"])
    
    # Get filter parameters from request
    report_types = request.args.getlist('type')
    tags = request.args.getlist('tag')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Search reports with query and filters
    reports = db_queries.search_reports(
        query=query,
        report_types=report_types, 
        tags=tags,
        start_date=start_date,
        end_date=end_date
    )
    
    # Pass both reports and filter selections back to the template
    return render_template("home.html", 
        reports=reports,
        query=query,
        selected_types=report_types,
        selected_tags=tags,
        start_date=start_date,
        end_date=end_date,
        user_type = session["user_type"]
    )


@app.route("/report/<int:report_id>")
def report(report_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    report = db_queries.get_report_by_id(report_id)
    return render_template("report.html", report=report, user_type = session["user_type"])



@app.route("/submit_report", methods=["GET", "POST"])
def submit_report():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        # Get form data
        title = request.form.get('title')
        report_type = request.form.get('report_type')
        description = request.form.get('description')
        report_link = request.form.get('report_link')
        supervisor = request.form.get('supervisor_id')
        
        # Get authors (may be multiple)
        authors = request.form.getlist('authors[]')
        
        # Get tags (split by comma)
        tags_input = request.form.get('tags')
        tags = tags_input.split(',') if tags_input else []
        tags = [tag.strip() for tag in tags if tag.strip()]
        
        # Handle file upload
        file_id = None
        if 'pdf_file' in request.files and request.files['pdf_file'].filename:
            pdf_file = request.files['pdf_file']
 
            import uuid
            file_id = f"{uuid.uuid4()}.pdf"

            upload_folder = "/home/soikot/Documents/files"

            file_path = os.path.join(upload_folder, file_id)
            pdf_file.save(file_path)
        
        # Validate required fields
        if not title or not report_type or not authors or not supervisor:
            # Get supervisors and common tags for the form
            supervisors = db_queries.get_all_supervisors()
            common_tags = db_queries.get_common_tags()
            return render_template("submit_report.html", 
                                 error='Please fill in all required fields with valid information.',
                                 supervisors=supervisors,
                                 common_tags=common_tags,
                                 user_type = session["user_type"]
                                 )
        
        # Submit the report to database
        submission_status = db_queries.submit_new_report(
            title=title,
            report_type=report_type,
            authors=authors,
            supervisor=supervisor,
            summary=description,
            link=report_link,
            file_id=file_id,
            tags=tags,
            submitter_id=session["user_id"]
        )
        
        if submission_status is True:
            flash('Report submitted successfully. It will be reviewed by the supervisor.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Error submitting report. Please try again.', 'error')
            return redirect(url_for('submit_report'))
    
    # For GET requests, show the submission form
    supervisors = db_queries.get_all_supervisors()
    common_tags = db_queries.get_common_tags()
    
    return render_template("submit_report.html", 
                         supervisors=supervisors,
                         common_tags=common_tags,
                         user_type = session["user_type"])


@app.route("/submissions")
def submissions():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    reports = db_queries.get_submitted_reports_by_user(session["user_id"])
    
    return render_template("submissions.html", reports=reports, user_type = session["user_type"])


@app.route("/reviews")
def reviews():
    if "user_id" not in session or session["user_type"] != 'teacher':
        return redirect(url_for("login"))
    
    pending_reports, reviewed_reports = db_queries.get_submitted_reports_by_supervisor(session["user_id"])

    return render_template("reviews.html", 
                           pending_reports=pending_reports, 
                           reviewed_reports=reviewed_reports)


@app.route("/report_review/<int:report_id>", methods=["GET", "POST"])
def report_review(report_id):
    if "user_id" not in session or session["user_type"] != 'teacher':
        return redirect(url_for("login"))
    
    if request.method == "POST":
        decision = request.form.get("decision")
        allow_pdf = request.form.get("allow_pdf")
        comment = request.form.get("comment", "")
        
        
        # Validate required fields
        if not decision:
            flash("Please select a decision.", "error")
            report = db_queries.get_report_by_id(report_id)
            return render_template("report_review.html", report=report, user_type=session["user_type"])
        
        # Submit the review
        success = db_queries.submit_report_review(
            report_id=report_id,
            reviewer_id=session["user_id"],
            decision=decision,
            pdf_allowed=allow_pdf,
            comment=comment
        )
        
        if success:
            flash("Review submitted successfully!", "success")
            return redirect(url_for("reviews"))
        else:
            flash("An error occurred while submitting the review. Please try again.", "error")
            
    report = db_queries.get_report_by_id(report_id)
    return render_template("report_review.html", report=report, user_type=session["user_type"])


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