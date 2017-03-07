import utilities
import json
from JiraApi import jira_create_issues, create_meta, search_issues, get_issue

# create issues/stories update Status
filename = "jira-import-template.xlsx"
s = utilities.login()
wb = utilities.readFile(filename)
issues = utilities.parseFile(wb, session=s, filename=filename)
utilities.create_issues(s, issues, filename)
