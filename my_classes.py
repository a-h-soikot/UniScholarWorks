
class Report:
    def __init__ (self):
        self.title = ""
        self.authors = []
        self.tags = []
        self.summary = ""
        self.report_id = 0
        self.date = None
    
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