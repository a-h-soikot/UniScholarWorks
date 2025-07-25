import os


# User Class
class User:
    def __init__(self):
        self.user_id = ""
        self.email = ""
        self.name = ""
        self.role = ""
        
    # Setters
    def set_user_id(self, user_id):
        self.user_id = user_id
        
    def set_email(self, email):
        self.email = email
        
    def set_name(self, name):
        self.name = name
        
    def set_role(self, role):
        self.role = role
        
    # Getters
    def get_user_id(self):
        return self.user_id
        
    def get_email(self):
        return self.email
        
    def get_name(self):
        return self.name
        
    def get_role(self):
        return self.role
    

# Report Class
class Report:
    def __init__ (self):
        self.title = ""
        self.authors = []
        self.tags = []
        self.summary = ""
        self.report_id = 0
        self.date = None
        self.link = ""
        self.file_id = ""
        self.supervisor = ""
        self.decision = None
        self.pdf_allowed = False
        self.comment = ""
        self.report_type = ""
        self.pdf_allowed = False
        self.report_status = ""
        self.submitter_id = ""
        self.comment = ""
    
    # Setters
    def set_title(self, title):
        self.title = title

    def set_authors(self, authors):
        self.authors = authors

    def set_tags(self, tags):
        self.tags = tags

    def set_summary(self, summary):
        self.summary = summary

    def set_report_id(self, report_id):
        self.report_id = report_id
    
    def set_date(self, date):
        self.date = date

    def set_link(self, link):
        self.link = link

    def set_file_id(self, file_id):
        if file_id is not None:
            self.file_id = file_id
            
    def set_decision(self, decision):
        self.decision = decision
        
    def set_pdf_allowed(self, pdf_allowed):
        self.pdf_allowed = pdf_allowed
        
    def set_comment(self, comment):
        self.comment = comment

    def set_supervisor(self, supervisor):
        self.supervisor = supervisor

    def set_report_type(self, report_type):
        self.report_type = report_type
    
    def set_pdf_allowed(self, allowed):
        if allowed == 'yes':
            self.pdf_allowed = True
        else:
            self.pdf_allowed = False

    def set_report_status(self, status):
        self.report_status = status  

    def set_submitter_id(self, submitter_id):
        self.submitter_id = submitter_id

    def set_comment(self, comment):
        if comment:
            self.comment = comment

    # Getters
    def get_title(self):
        return self.title
    
    def get_authors(self):
        return self.authors
    
    def get_tags(self):
        return self.tags
    
    def get_summary(self):
        return self.summary
    
    def get_report_id(self):
        return self.report_id
    
    def get_date(self):
        return self.date.strftime("%d %B %Y")
    
    def get_link(self):
        return self.link
    
    def get_file_id(self):
        return self.file_id
        
    def get_decision(self):
        return self.decision
        
    def get_pdf_allowed(self):
        return self.pdf_allowed
        
    def get_comment(self):
        return self.comment

    def get_supervisor(self):
        return self.supervisor
    
    def get_report_type(self):
        return self.report_type.capitalize()
    
    def is_pdf_allowed(self):
        return self.pdf_allowed
    
    def pdf_exists(self):
        if self.file_id is None or self.file_id == "":
            return False
        directory = "/home/soikot/Documents/files"
        file_path = os.path.join(directory, self.file_id)
        if not os.path.exists(file_path):
            return False
        return True

    def get_report_status(self):
        return self.report_status.capitalize()

    def get_submitter_id(self):
        return self.submitter_id
    
    def get_comment(self):
        if len(self.comment) < 1:
            return None
        
        return self.comment
    
    # -----------------------------------------------

    def delete_pdf(self):
        if self.file_id is None or self.file_id == "":
            return None
        directory = "/home/soikot/Documents/files"
        file_path = os.path.join(directory, self.file_id)
        if not os.path.exists(file_path):
            return None
        try:
            os.remove(file_path)
            self.file_id = ""

        except Exception as e:
            print(f"Error deleting file: {e}")
            return None