import utilities
import json
from JiraApi import create_issues, create_meta

# opening workbook & associated sheets

# print(create_issues(issues))

# utilities.run()
filename = "arbor.xlsx"
s = utilities.login()
wb = utilities.readFile(filename)
issues = utilities.parseFile(wb, s, filename)

create_issues(s, issues)
# issue_response = json.loads(create_issues(s, issues).text)
# utilities.write_jira_key(issue_response, len(issues))
# print(issue)
# print(issue['issues'][0]['key'])

# print(issue.text)


# meta = create_meta(s)
# data = utilities.get_issuetypes(meta.text)
# print(str(data))
# print(meta)
# print(meta.text)
