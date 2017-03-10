class Story:
    def __init__(self, key="", summary=None, description=None,
                 project=None, customer=None, assignee=None, board=None,
                 sprint=None, col=None):
        self.key = key  # if key is not None else ""
        self.summary = summary if summary is not None else ""
        self.description = description if description is not None else ""
        self.project = project if project is not None else ""
        self.customer = customer if customer is not None else ""
        self.assignee = assignee if assignee is not None else ""
        self.board = board if board is not None else ""
        self.sprint = sprint if sprint is not None else ""
        self.col = col if col is not None else ""

    def __str__(self):
        return ('key: ' + self.key + '\nsummary: ' + self.summary +
                '\ndescription: ' + self.description + '\nproject: ' +
                self.project + '\ncol: ' + self.col + '\n')
