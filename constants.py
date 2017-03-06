APPLICATION_JSON = {'Content-Type': 'application/json'}
URL = "https://jonastemborski.atlassian.net"  # Test Environment
# URL = "http://jira.spartasystems.com"  # Production Environment

URL_BROWSE = URL + '/browse/'

# REST API
URI_LOGIN = URL + '/rest/auth/1/session'
URI_CREATE_META = URL + '/rest/api/2/issue/createmeta'
URI_CREATE_ISSUE = URL + '/rest/api/2/issue'
URI_CREATE_ISSUES = URL + '/rest/api/2/issue/bulk'
URI_SEARCH = '/rest/api/2/search'
URI_GET_ALL_PROJECTS = '/rest/api/2/project'
URI_MOVE_ISSUES_TO_SPRINT = '/rest/agile/1.0/sprint/'  # '{sprintId}/issue'
URI_SEARCH = URL + '/rest/api/2/search'
URI_GET_ISSUE = URL + '/rest/api/2/issue'  # {issueIdOrKey}  
