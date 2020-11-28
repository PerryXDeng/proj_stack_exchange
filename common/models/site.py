
class Site():
    site_count = 0  # this should be handled outside of the site class because
                    # then we can reuse this class for reading from database if we want

    def __init__(self, name):
        self.site_count += 1
        self.id = self.site_count
        self.name = name

    def __str__(self):
        return f"site: {{id : {self.id} , name: {self.name}}}"
