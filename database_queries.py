import mysql.connector
from my_classes import Report

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'uni_scholar_works'
}


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