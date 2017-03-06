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
