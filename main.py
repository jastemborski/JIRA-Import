import utilities
import json
from JiraApi import jira_create_issues, create_meta, search_issues, get_issue
from JiraApi import move_issues_to_sprint


"""==========================================================================
|               create issues/stories update Status                         |
=========================================================================="""

# filename = "jira-import-template.xlsx"
s = utilities.login()
# wb = utilities.readFile(filename)
# issues = utilities.parseFile(wb, session=s, filename=filename)
# utilities.create_issues(s, issues, filename)
utilities.move_to_sprint(s, "TEST board", "TEST Sprint 15", "TEST-1112")
# move_issues_to_sprint("15", "TEST-1088", s)

"""==========================================================================
|                           Updates Stories                                 |
=========================================================================="""

# filename = "jira-import-template.xlsx"
# s = utilities.login()
# wb = utilities.readFile(filename)
# issues = utilities.parseFile(wb, session=s, filename=filename)
# utilities.update_status(issues, s, filename)

"""==========================================================================
|               Seach Queries                                               |
=========================================================================="""

# search_query = "project=TEST and summary=Complaint: Modify Field Values"
# field_list = []
# search_query = utilities.form_query(issues[0])
# field_list.append("summary, status")
# print(search_issues(search_query, field_list=field_list, session=s))
# search = json.loads(search_issues(search_query, field_list=field_list, session=s).text)
# print(search['issues'][0]['key'])


"""==========================================================================
|               Create Meta Data                                            |
=========================================================================="""

# meta = create_meta(s)
# data = utilities.get_issuetypes(meta.text)
# print(str(data))
# print(meta)
# print(meta.text)
