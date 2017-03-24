class Issue:

    def __init__(self, change_type=None, change_description=None,
                 platform=None, process=None, parent=None, customer=None,
                 project_key=None, notes=None, custom_fields=None,
                 issue_type=None, status=None, jira_key=None, row=None,
                 board=None, sprint=None, assignee=""):
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
        self.row = row if row is not None else ""
        self.board = board if board is not None else ""
        self.sprint = sprint if sprint is not None else ""
        self.assignee = assignee

    def __str__(self):
        return(self.change_type + " " + self.change_description + " " +
               self.platform + " " + self.process)


class IssueTypeMeta:

    def __init__(self, url=None, id=None, description=None,
                 name=None, subtask=False):
        self.url = url if url is not None else ""
        self.id = id if id is not None else ""
        self.description = description if description is not None else ""
        self.name = name if name is not None else ""
        self.subtask = subtask

    def __str__(self):
        return(self.name)


class ProjectMeta:

    def __init__(self, url=None, id=None, key=None, name=None, issuetype=None):
        self.url = url if url is not None else ""
        self.id = id if id is not None else ""
        self.key = key if key is not None else ""
        self.name = name if name is not None else ""
        self.issuetype = issuetype if issuetype is not None else []

    def __str__(self):
        return(self.name)

    def issuetype(self, issuetype):
        self.__issuetype = IssueTypeMeta.__init__(self,
                                                  issuetype.url,
                                                  issuetype.id,
                                                  issuetype.description,
                                                  issuetype.name)
