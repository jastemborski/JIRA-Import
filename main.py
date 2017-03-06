import utilities
import json
from JiraApi import create_issues, create_meta, search_issues, get_issue


# filename = "jira-import-template.xlsx"
# s = utilities.login()
# wb = utilities.readFile(filename)
# issues = utilities.parseFile(wb, session=s, filename=filename)
# issue_response = json.loads(create_issues(s, issues).text)
# utilities.write_jira_key(issue_response, len(issues), filename)
# utilities.write_status(issue_response, len(issues), filename, s)

filename = "jira-import-template.xlsx"
s = utilities.login()
wb = utilities.readFile(filename)
issues = utilities.parseFile(wb, session=s, filename=filename)
utilities.update_status(issues, s, filename)



# search_query = "project=TEST and summary=Complaint: Modify Field Values"
# field_list = []
# search_query = utilities.form_query(issues[0])
# field_list.append("summary, status")


# print(search_issues(search_query, field_list=field_list, session=s))
# search = json.loads(search_issues(search_query, field_list=field_list, session=s).text)
# print(search['issues'][0]['key'])


# print(issue)
# print(issue['issues'][0]['key'])

# print(issue.text)


# meta = create_meta(s)
# data = utilities.get_issuetypes(meta.text)
# print(str(data))
# print(meta)
# print(meta.text)
