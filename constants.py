"""==================================================================
|						Environment Variables       	  			|
=================================================================="""

# SUBTASK = "5"  # Prod
# STORY = "10001"  # Prod
# PROJECT_KEY = "DELIVERCOM"  # Prod
# URL = "http://jira.spartasystems.com"  # Production Environment

SUBTASK = "10102"  # Test
STORY = "10100"  # Test
PROJECT_KEY = "TEST"  # Test
URL = "https://jonastemborski.atlassian.net"  # Test Environment

"""==================================================================
|					   End Environment Variables         			|
=================================================================="""


"""==================================================================
|							REST API 								|
=================================================================="""

APPLICATION_JSON = {'Content-Type': 'application/json'}
ID_JIRA_PROCESS = 'customfield_10401'
ID_JIRA_PLATFORM = 'customfield_10400'
URL_BROWSE = URL + '/browse/'

URI_LOGIN = URL + '/rest/auth/1/session'
URI_CREATE_META = URL + '/rest/api/2/issue/createmeta'
URI_CREATE_ISSUE = URL + '/rest/api/2/issue'
URI_CREATE_ISSUES = URL + '/rest/api/2/issue/bulk'
URI_SEARCH = '/rest/api/2/search'
URI_GET_ALL_PROJECTS = '/rest/api/2/project'
URI_SEARCH = URL + '/rest/api/2/search'
URI_GET_ISSUE = URL + '/rest/api/2/issue'  # {issueIdOrKey}
URI_GET_ALL_BOARDS = URL + '/rest/agile/1.0/board/'
URI_GET_ALL_SPRINTS = URL + '/rest/agile/1.0/board/'  # '{boardid}/sprint'
URI_MOVE_ISSUES_TO_SPRINT = URL + '/rest/agile/1.0/sprint/'  # '{sprintId}/issue'

"""==================================================================
|						End REST API 								|
=================================================================="""
