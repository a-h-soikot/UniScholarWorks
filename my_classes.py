import os

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
        self.report_type = ""
        self.pdf_allowed = False
    
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
        if self.pdf_allowed and file_id is not None:
            self.file_id = file_id

    def set_supervisor(self, supervisor):
        self.supervisor = supervisor

    def set_report_type(self, report_type):
        self.report_type = report_type
    
    def set_pdf_allowed(self, allowed):
        if allowed == 'yes':
            self.pdf_allowed = True
        else:
            self.pdf_allowed = False
        

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