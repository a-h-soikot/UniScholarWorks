import mysql.connector
from my_classes import Report, User

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'uni_scholar_works'
}


def get_user_by_credentials(user_id, password):
    """
    Authenticate a user by user_id/email and password
    Returns a User object if credentials are valid, None otherwise
    """
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    #hashed_password = hashlib.sha256(password.encode()).hexdigest()

    query = """
    SELECT * FROM students
    WHERE (student_id = %s OR email = %s) AND password = %s
    """
    cursor.execute(query, (user_id, user_id, password))
    
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user_data:
        user = User()
        user.set_user_id(user_data['student_id'])
        user.set_email(user_data['email'])
        user.set_name(user_data['name'])
        
        return user
    
    return None


def get_reports():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # dictionary=True gives column names

    # Fetch all reports
    cursor.execute("SELECT reports.report_id, title, summary, review_date FROM reports inner join reviews on reports.report_id = reviews.report_id where reviews.decision = 'accepted' order by review_date desc")
    reports = cursor.fetchall()

    reports_list = []

    for row in reports:

        report = Report()

        report.set_report_id(row['report_id'])
        report.set_title(row['title'])
        report.set_summary(row['summary'])
        report.set_date(row['review_date'])

        cursor.execute("SELECT name from students where student_id in (SELECT student_id from report_authors  WHERE report_id = %s)", (row['report_id'], ))
        authors = cursor.fetchall()
        report.set_authors([author['name'] for author in authors])

        cursor.execute("SELECT tag from report_tag WHERE report_id = %s", (row['report_id'], ))
        tags = cursor.fetchall()
        report.set_tags([tag['tag'] for tag in tags])

        reports_list.append(report)

    cursor.close()
    conn.close()

    return reports_list

def get_report_by_id(report_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Fetch report by ID
    cursor.execute("SELECT * FROM reports WHERE report_id = %s", (report_id,))
    row = cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()
        return None

    report = Report()
    report.set_report_id(row['report_id'])
    report.set_title(row['title'])
    report.set_summary(row['summary'])
  
    report.set_link(row['link'])
    report.set_supervisor(row['supervisor'])
    report.set_report_type(row['type'])

    cursor.execute("SELECT name FROM students WHERE student_id IN (SELECT student_id FROM report_authors WHERE report_id = %s)", (report_id,))
    authors = cursor.fetchall()
    report.set_authors([author['name'] for author in authors])

    cursor.execute("SELECT tag FROM report_tag WHERE report_id = %s", (report_id,))
    tags = cursor.fetchall()
    report.set_tags([tag['tag'] for tag in tags])

    cursor.execute("SELECT review_date, pdf_allowed FROM reviews WHERE report_id = %s", (report_id,))
    review = cursor.fetchone()
    report.set_date(review['review_date'])
    report.set_pdf_allowed(review['pdf_allowed'])

    report.set_file_id(row['file_id'])

    cursor.close()
    conn.close()

    return report