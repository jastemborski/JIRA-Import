class Issue:

    def __init__(self, change_type=None, change_description=None,
                 platform=None, process=None, parent=None, customer=None,
                 project_key=None, notes=None, custom_fields=None,
                 issue_type=None, status=None, jira_key=None):
        self.change_type = change_type if change_type is not None else ""
        self.change_description = change_description if \
            change_description is not None else ""
        self.platform = platform if platform is not None else ""
        self.process = process if process is not None else ""
        self.parent = parent if parent is not None else ""
        self.customer = customer if customer is not None else ""
        self.project_key = project_key if project_key is not None else ""
        self.notes = notes if notes is not None else ""
        self.custom_fields = custom_fields if custom_fields is not None else []
        self.issue_type = issue_type if issue_type is not None else ""
        self.status = status if status is not None else "",
        self.jira_key = jira_key if jira_key is not None else "",

    def __str__(self):
        return(self.change_type + " " + self.change_description + " " +
               self.platform + " " + self.process)
