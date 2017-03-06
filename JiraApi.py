from Issue import Issue
import constants
import json

# SUBTASK = "5"  # Prod
# STORY = "10001"  # Prod

SUBTASK = "10102"  # Test
STORY = "10100"  # Test


def create_issue(issue, post=False, session=None):
    # issue is a subtask
    if len(issue.parent) is not 0:
        parent = '"parent":{"key":"' + issue.parent + '"},'
        summary = issue.process + ': ' + issue.change_type

        # Test Fields
        custom_fields = ', "customfield_10200": ["' + issue.customer + '"], \
                        "customfield_10300": ["' + issue.process + '"], \
                        "customfield_10301": ["' + issue.platform + '"]'

        # prod fields
        # custom_fields = ', "customfield_12904": ["' + issue.customer + '"], \
        #                  "customfield_12906": "' + issue.process + '", \
        #                  "customfield_13008": "' + issue.platform + '"'
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
             ","issuetype":{"id":' + issuetype + '}' + custom_fields + '}}'
    # print(jIssue)

    if not post:
        return json.loads(jIssue)
    else:
        return session.post(constants.URI_CREATE_ISSUE,
                            headers=constants.APPLICATION_JSON,
                            json=(json.loads(jIssue)))


def create_issues(session, Issues):
    jIssues = ""
    for issue in Issues:
        jIssues += json.dumps(create_issue(issue, session=session))
        if issue is not Issues[-1]:
            jIssues += ','
        # jIssues = temp_issue + ','
    jIssues = '{"issueUpdates":[' + jIssues + ']}'
    # return jIssues
    print(jIssues)
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
