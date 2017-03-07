import utilities
import json
from JiraApi import create_issues


# create issues/stories update Status
filename = "jira-import-template.xlsx"
s = utilities.login()
wb = utilities.readFile(filename)
issues = utilities.parseFile(wb, session=s, filename=filename)
issue_response = json.loads(create_issues(s, issues).text)
utilities.write_jira_key(issue_response, len(issues), filename)
utilities.write_status(issue_response, len(issues), filename, s)
