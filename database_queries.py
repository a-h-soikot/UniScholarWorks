from flask import flash
import mysql.connector
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from my_classes import Report, User

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'uni_scholar_works'
}


def get_user_by_credentials(user_id, password, user_type):
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT * FROM students
    WHERE (student_id = %s OR email = %s)
    """

    if user_type == "teacher":
        query = """
        SELECT * FROM teachers
        WHERE (teacher_id = %s OR email = %s)
        """
    cursor.execute(query, (user_id, user_id))
    
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    try:
        if user_data and PasswordHasher().verify(user_data['password'], password):
            user = User()
            user.set_user_id(user_data['student_id'] if user_type == "student" else user_data['teacher_id'])
            user.set_email(user_data['email'])
            user.set_name(user_data['name'])
            
            return user
    
    except VerifyMismatchError:
        return None
    
    return None


def search_reports(query, page, per_page, report_types=None, tags=None, start_date=None, end_date=None):

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    offset = (page - 1) * per_page

    # Base query
    query_sql = """
    SELECT DISTINCT reports.report_id, title, summary, review_date 
    FROM reports 
    INNER JOIN reviews ON reports.report_id = reviews.report_id
    """
    
    conditions = ["reviews.decision = 'accepted'"]
    params = []
    
    # Add search conditions
    if query and query.strip():
      
        search_terms = query.split()
        search_conditions = []
        
        for term in search_terms:
            search_term = f"%{term}%"
            
            # Combine conditions with OR for the same term
            term_condition = """
                (reports.title LIKE %s OR 
                reports.summary LIKE %s)
            """
            params.extend([search_term, search_term])
            
            search_conditions.append(term_condition)
        
        # Join all search terms with AND
        if search_conditions:
            conditions.append("(" + " AND ".join(search_conditions) + ")")
    
    # Add type filter
    if report_types and len(report_types) > 0:
        type_placeholders = ', '.join(['%s'] * len(report_types))
        conditions.append(f"reports.type IN ({type_placeholders})")
        params.extend(report_types)
    
    # Add tag filter
    if tags and len(tags) > 0:
        query_sql += " INNER JOIN report_tag ON reports.report_id = report_tag.report_id"
        tag_placeholders = ', '.join(['%s'] * len(tags))
        conditions.append(f"report_tag.tag IN ({tag_placeholders})")
        params.extend(tags)
    
    # Add date filters
    if start_date:
        conditions.append("DATE(reviews.review_date) >= %s")
        params.append(start_date)
    
    if end_date:
        conditions.append("DATE(reviews.review_date) <= %s")
        params.append(end_date)
    
    # Add all conditions to the query
    if conditions:
        query_sql += " WHERE " + " AND ".join(conditions)
    
    # Add ordering
    query_sql += " ORDER BY review_date DESC"
    
    query_sql += " LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    cursor.execute(query_sql, params)
    rows = cursor.fetchall()
    
    reports_list = []
    
    for row in rows:
        report = Report()
        
        report.set_report_id(row['report_id'])
        report.set_title(row['title'])
        report.set_summary(row['summary'])
        report.set_date(row['review_date'])
        
        # Get authors
        cursor.execute("""
            SELECT name FROM students 
            WHERE student_id IN (
                SELECT student_id FROM report_authors 
                WHERE report_id = %s
            )
        """, (row['report_id'],))
        
        authors = cursor.fetchall()
        report.set_authors([author['name'] for author in authors])
        
        # Get tags
        cursor.execute("SELECT tag FROM report_tag WHERE report_id = %s", (row['report_id'],))
        tags = cursor.fetchall()
        report.set_tags([tag['tag'] for tag in tags])
        
        # Report type
        cursor.execute("SELECT type FROM reports WHERE report_id = %s", (row['report_id'],))
        report_type = cursor.fetchone()
        if report_type:
            report.set_report_type(report_type['type'])
        
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

    cursor.execute("SELECT review_date, pdf_allowed, decision, comment FROM reviews WHERE report_id = %s", (report_id,))
    review = cursor.fetchone()
    if review:
        report.set_date(review['review_date'])
        report.set_pdf_allowed(review['pdf_allowed'])
        report.set_decision(review['decision'])
        report.set_comment(review['comment'])

    report.set_file_id(row['file_id'])

    cursor.close()
    conn.close()

    return report
    
def submit_new_report(title, report_type, authors, supervisor, summary=None, link=None, file_id=None, tags=None, submitter_id=None):
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    try:
        conn.start_transaction()
        
        # Insert report
        cursor.execute("""
            INSERT INTO reports (title, summary, type, supervisor, link, file_id, submitter_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (title, summary, report_type, supervisor, link, file_id, submitter_id))
        
        report_id = cursor.lastrowid
        
        # Insert authors
        for author_id in authors:
            cursor.execute("SELECT student_id FROM students WHERE student_id = %s", (author_id,))
            result = cursor.fetchone()
            
            if result:
                student_id = result[0]
            else:
                flash(f"Student/Author with ID '{author_id}' not found in the database.", 'error')
                return False
            
            # Link author to report
            cursor.execute("""
                INSERT INTO report_authors (report_id, student_id)
                VALUES (%s, %s)
            """, (report_id, student_id))
        
        # Insert tags
        if tags:
            for tag in tags:
                cursor.execute("""
                    INSERT INTO report_tag (report_id, tag)
                    VALUES (%s, %s)
                """, (report_id, tag))
        

        # Commit transaction
        conn.commit()
        
        return True
        
    except Exception as e:
        conn.rollback()
        flash(f"Error submitting report: {str(e)}", 'error')
        return False
    finally:
        cursor.close()
        conn.close()
        
def get_all_supervisors():
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT teacher_id, name FROM teachers")
    supervisors = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return supervisors

def get_common_tags():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT tag, COUNT(*) as count 
        FROM report_tag 
        GROUP BY tag 
        ORDER BY count DESC 
        LIMIT 10
    """)
    tags = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return [t['tag'] for t in tags]



def get_submitted_reports_by_user(user_id):

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT reports.report_id, title, summary, submitter_id, submission_date, comment FROM reports
        LEFT JOIN reviews ON reports.report_id = reviews.report_id
        WHERE submitter_id = %s
        order by report_id DESC
    """, (user_id,))
    
    rows = cursor.fetchall()
    
    reports_list = []
    
    for row in rows:
        report = Report()
        
        report.set_report_id(row['report_id'])
        report.set_title(row['title'])
        report.set_summary(row['summary'])
        report.set_date(row['submission_date'])
        report.set_submitter_id(row['submitter_id'])
        report.set_comment(row['comment'])
        
        # Get authors
        cursor.execute("""
            SELECT name FROM students 
            WHERE student_id IN (
                SELECT student_id FROM report_authors 
                WHERE report_id = %s
            )
        """, (row['report_id'],))
        
        authors = cursor.fetchall()
        report.set_authors([author['name'] for author in authors])
        
        # Get tags
        cursor.execute("SELECT tag FROM report_tag WHERE report_id = %s", (row['report_id'],))
        tags = cursor.fetchall()
        report.set_tags([tag['tag'] for tag in tags])
        
        # Get submission status
        cursor.execute("SELECT decision FROM reviews WHERE report_id = %s", (row['report_id'],))
        review = cursor.fetchone()
        if review:
            report.set_report_status(review['decision'])
        else:
            report.set_report_status("pending")

        reports_list.append(report)
    

    cursor.close()
    conn.close()
    
    return reports_list


def get_submitted_reports_by_supervisor(supervisor_id):

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT reports.report_id, title, supervisor, summary, submitter_id, submission_date, comment FROM reports
        LEFT JOIN reviews ON reports.report_id = reviews.report_id
        WHERE supervisor = %s
        order by report_id DESC
    """, (supervisor_id,))
    
    rows = cursor.fetchall()

    pending_reports_list = []
    reviewed_reports_list = []

    for row in rows:
        report = Report()
        
        report.set_report_id(row['report_id'])
        report.set_title(row['title'])
        report.set_summary(row['summary'])
        report.set_date(row['submission_date'])
        report.set_submitter_id(row['submitter_id'])
        report.set_comment(row['comment'])
        
        # Get authors
        cursor.execute("""
            SELECT name FROM students 
            WHERE student_id IN (
                SELECT student_id FROM report_authors 
                WHERE report_id = %s
            )
        """, (row['report_id'],))
        
        authors = cursor.fetchall()
        report.set_authors([author['name'] for author in authors])
        
        # Get tags
        cursor.execute("SELECT tag FROM report_tag WHERE report_id = %s", (row['report_id'],))
        tags = cursor.fetchall()
        report.set_tags([tag['tag'] for tag in tags])
        
        # Get submission status
        cursor.execute("SELECT decision FROM reviews WHERE report_id = %s", (row['report_id'],))
        review = cursor.fetchone()
        if review:
            report.set_report_status(review['decision'])
            reviewed_reports_list.append(report)
        else:
            report.set_report_status("pending")
            pending_reports_list.append(report)

        
    
    cursor.close()
    conn.close()

    return pending_reports_list, reviewed_reports_list
    

def submit_report_review(report_id, reviewer_id, decision, pdf_allowed, comment=None):
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    try:
        # Insert new review
        cursor.execute("""
            INSERT INTO reviews (report_id, teacher_id, decision, pdf_allowed, comment)
            VALUES (%s, %s, %s, %s, %s)
            """, (report_id, reviewer_id, decision, pdf_allowed, comment))
        
        if decision == "rejected":
            cursor.execute("""
                UPDATE reports 
                SET file_id = '', link = ''
                WHERE report_id = %s
            """, (report_id,))
        
        elif pdf_allowed == 'no':
            cursor.execute("""
                UPDATE reports 
                SET file_id = ''
                WHERE report_id = %s
            """, (report_id,))

        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback()
        flash(f"Error submitting review: {str(e)}", 'error')
        return False
    finally:
        cursor.close()
        conn.close()


def get_pending_review_count(teacher_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT COUNT(reports.report_id) as count 
        FROM reports LEFT JOIN reviews on reports.report_id = reviews.report_id
        WHERE reviews.decision IS NULL AND reports.supervisor = %s
    """, (teacher_id,)) 
    
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return result['count'] if result else 0