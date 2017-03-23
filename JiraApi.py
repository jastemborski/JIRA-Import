from Issue import Issue
import constants
import json

SUBTASK = "5"  # Prod
STORY = "10001"  # Prod

# SUBTASK = "10102"  # Test
# STORY = "10100"  # Test


def jira_create_issue(issue, post=False, session=None):
    # issue is a subtask
    optional_fields = ', "assignee": { "name":"' + issue.assignee + '"} ' \
                      if issue.assignee else ""
    if len(issue.parent) is not 0:
        parent = '"parent":{"key":"' + issue.parent + '"},'
        summary = issue.process + ': ' + issue.change_type

        # Test Fields
        # custom_fields = ', "customfield_10200": ["' + issue.customer + '"], \
        #                 "' + constants.ID_JIRA_PROCESS + '": "' \
        #                 + issue.process + '", "' + constants.ID_JIRA_PLATFORM + '": \
        #                 "' + issue.platform + '"'

        # prod fields
        custom_fields = ', "customfield_12904": ["' + issue.customer + '"], \
                         "customfield_12906": "' + issue.process + '", \
                         "customfield_13008": "' + issue.platform + '"'
        issuetype = SUBTASK
    # issue is a story
    else:
        parent = issue.parent
        summary = issue.customer + ': ' + issue.process
        custom_fields = ""
        issuetype = STORY
    jIssue = '{"update":{}, "fields":{"project":{"key": "' \
             + issue.project_key + '"},' + parent + '"summary": "' + summary + '", \
             "description": "' + issue.change_description + ' \
             ","issuetype":{"id":' + issuetype + '}' \
             + custom_fields + optional_fields + '}}'
    if not post:
        return json.loads(jIssue)
    else:
        return session.post(constants.URI_CREATE_ISSUE,
                            headers=constants.APPLICATION_JSON,
                            json=(json.loads(jIssue)))


def jira_create_issues(session, issues):
    jIssues = ""
    for issue in issues:
        # print("test1")
        # json.dumps(jira_create_issue(issue))
        temp = json.dumps(jira_create_issue(issue))
        jIssues = jIssues + temp
        if issue is not issues[-1]:
            jIssues += ','
        # jIssues = temp_issue + ','
    jIssues = '{"issueUpdates":[' + jIssues + ']}'
    # return jIssues
    return session.post(constants.URI_CREATE_ISSUES,
                        headers=constants.APPLICATION_JSON,
                        json=(json.loads(jIssues)))


def create_meta(session, project_id=None, project_keys=None,
                issue_type_ids=None, issue_type_names=None):
    return session.get(constants.URI_CREATE_META,
                       headers=constants.APPLICATION_JSON)

# def move_issues_to_sprint(session, issues_ids):
#     for issue in issue_ids:

# def get_issue()


def search_issues(search_query, field_list=None, start="0", max_results="15",
                  fields_by_key="true", session=None):
    fields = ""
    for field in field_list:
        fields = '"' + field + '"'
        if field is not field_list[-1]:
            fields = fields + ', '
    query = '{ "jql": "' + search_query + '", "startAt": ' + start + ',' \
            '"maxResults": ' + max_results + ', "fields": [' + fields + \
            '], "fieldsByKeys":' + fields_by_key + '}'
    # return query
    return session.post(constants.URI_SEARCH,
                        headers=constants.APPLICATION_JSON,
                        json=(json.loads(query)))


def get_issue(key, session):
    return session.get((constants.URI_GET_ISSUE + '/' + key),
                       headers=constants.APPLICATION_JSON)


def move_issues_to_sprint(sprint_id, jira_key, session):
    query = '{ "issues": ["' + jira_key + '"]}'
    return session.post((constants.URI_MOVE_ISSUES_TO_SPRINT + sprint_id +
                         '/issue'),
                        headers=constants.APPLICATION_JSON,
                        json=(json.loads(query)))


def get_all_boards(session):
    return session.get(constants.URI_GET_ALL_BOARDS,
                       headers=constants.APPLICATION_JSON)


def get_all_sprints(board_id, session):
    return session.get(constants.URI_GET_ALL_BOARDS + str(board_id) +
                       '/sprint',
                       headers=constants.APPLICATION_JSON)
