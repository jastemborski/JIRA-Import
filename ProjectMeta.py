from IssueTypeMeta import IssueTypeMeta


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
