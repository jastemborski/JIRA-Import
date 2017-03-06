from Issue import Issue
import openpyxl
from JiraApi import create_issues, create_issue
import requests
import constants
import json
import getpass
from ProjectMeta import ProjectMeta
from IssueTypeMeta import IssueTypeMeta
from Story import Story
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.styles import Font, PatternFill, colors, Color


PROJECT_KEY = "TEST"
# PROJECT_KEY = "DELIVERCOM"
info_row = 2
PROCESS_DICT = {'Complaint': 'B', 'Inquiry': 'C', 'CAPA': 'D',
                'Quality Event': 'E', 'Quality Event Investigation': 'E',
                'Change Control': 'F', 'Change Control Plan': 'F',
                'Assessment': 'G', 'Investigation/Evaluation': 'H',
                'Audit': 'I', 'Audit Findings': 'I', 'Audit Plan': 'I',
                'Products': 'J', 'Contacts': 'K',
                'Notes': 'L', 'Tasks': 'M', 'Global': 'N',
                }

COL_DICT = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H',
            9: 'I', 10: 'J', 11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O',
            16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V',
            23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}


def get_change_type(req_sheet, row_num):
    return (req_sheet['A' + str(row_num)].value)


def get_change_description(req_sheet, row_num):
    return (req_sheet['B' + str(row_num)].value)


def get_platform(req_sheet, row_num):
    return (req_sheet['C' + str(row_num)].value)


def get_process(req_sheet, row_num):
    return (req_sheet['D' + str(row_num)].value)


def get_notes(req_sheet, row_num):
    return (req_sheet['E' + str(row_num)].value)


def get_customer(customer_sheet):
    return (customer_sheet['A' + "2"].value)


def get_parent(jira_sheet, process):
    # print(process + '\n')
    if process in PROCESS_DICT:
        return (jira_sheet[PROCESS_DICT.get(process) + "2"].value)
    else:
        print("""Error: " + process + " is an invalid process.
                The following QE processes are acceptable: Complaints, Inquiry,
                CAPA, Quality Event, Change Control.\n""")


def get_stories(jira_sheet, customer_sheet):
    """ Captures information residing in the JIRA Stories sheet of the Workbook

    Populates a list of Story objects corresponding to the data captured on the
    JIRA Stories sheet.

    Args:
        jira_sheet: A variable holding an Excel Workbook sheet in memory.
    Returns:
        story_list: A list of Story objects corresponding to
                  table row data fetched. For example:
                    key: TEST-303
                    summary: CAPA
                    description: CAPA module
                    project: TEST
                    col: D
    """
    story_list = []
    for c in range(2, jira_sheet.max_column):
        key = jira_sheet[COL_DICT[c] + "2"].value
        if key is None:
            key = ""
        # print(key)
        story = Story(key,  # key
                      jira_sheet[COL_DICT[c] + "3"].value,  # summary
                      jira_sheet[COL_DICT[c] + "4"].value,  # description
                      jira_sheet[COL_DICT[c] + "5"].value,  # project
                      customer_sheet['A2'].value,  # customer
                      COL_DICT[c])  # col
        story_list.append(story)
        # print(story.key)
    return story_list


def create_stories(story_dict, session=None, wb=None, filename=None):
    """ Creates JIRA Stories if not already created.

    Checks to see if the row 'Key', designating the JIRA Story key, has been
    populated - indicating the Story already exists within JIRA.

    If the story doesn't exist and both the 'Description' and 'Title'
    rows have been populated, indicating a Story should be created, - create
    the Stories the stories then update the Excel Workbook.

    Args:
        story_dict: A list of Story objects captured on the JIRA Stories sheet.
        session: A variable capturing the session info previously captured via
                the Login function. ( Optional )
        wb: A variable storing the Excel Workbook in memory. ( Optional )
    """
    try:
        for story in story_dict:
            # print(story.key)
            if not story.key:
                _issue = Issue()
                _issue.customer = story.customer
                _issue.project_key = PROJECT_KEY
                _issue.process = story.summary
                _issue.change_description = story.description
                if story.summary and story.description:
                    issue = create_issue(_issue, True, session)
                    print(issue)
                    print(issue.text)
                    info = json.loads(issue.text)
                    key = info['key']
                    write_story(wb, story.col, key, filename)
    except Exception:
        # raise Exception
        print("Invalid issue\n")


def write_story(wb, col, key, filename):
    """ Writes Stories to Excel Workbook.

    Args:
        wb: A variable storing the Excel Workbook in memory.
        col: A variable containing the column being updated.
        key: A variable containing the JIRA Story Key.
    """
    try:
        jira_sheet = wb.get_sheet_by_name('JIRA Stories')
        jira_sheet[col + "2"] = key
        wb.save(filename)
    except Exception:
        print("""Unable to save workbook. Please close excel spreadsheet then
               try again.""")


def readFile(filename=None):
    try:
        if filename is None:
            filename = input("Please enter a filename: ")
        wb = openpyxl.load_workbook(filename=filename)
        return wb
    except Exception:
        print("Invalid file name\n")


def parseFile(wb, session=None, filename=None):
    try:
        req_sheet = wb.get_sheet_by_name('Requirements')
        jira_sheet = wb.get_sheet_by_name('JIRA Stories')
        customer_sheet = wb.get_sheet_by_name('Customer Info')
        issues = []
        maxRow = req_sheet.max_row
        customer = get_customer(customer_sheet)

        # Determines if Stories have already been created for each Sub-task
        # stories = get_stories(jira_sheet, customer_sheet)
        # create_stories(stories, session, wb, filename)

        # # Process File
        for row in range(2, maxRow + 1):
            issue = Issue()
            issue.change_type = get_change_type(req_sheet, row)
            issue.change_description = get_change_description(req_sheet, row)
            issue.platform = str(get_platform(req_sheet, row))
            issue.process = str(get_process(req_sheet, row))
            issue.notes = get_notes(req_sheet, row)
            issue.parent = get_parent(jira_sheet, issue.process)
            issue.customer = customer
            issue.issue_type = "10102"
            issue.project_key = PROJECT_KEY
            issues.append(issue)
        return issues
    except Exception:
        print("Error processing file.")


def run():
    running = True
    run = 0
    while type(running) is not list:
        running = readFile()

    print('\nReading File')

    while run is not 2:
        run = input("""Please select one of the options:
                 1 - Create Issues
                 2 - Terminate Program \n""")
        print(options(run, running))


def login():
    authenticated = False
    while authenticated is not True:
        username = input("Please enter your JIRA username: ")
        password = getpass.getpass("Please enter your JIRA password: ")
        session = requests.Session()
        # session.auth = (username, password)
        cred = json.dumps({"username": username, "password": password})
        s = session.post(constants.URI_LOGIN,
                         headers=constants.APPLICATION_JSON,
                         data=cred)
        authenticated = s.ok
        if (not s.ok):
            print("""\nInvalid login credentials.
                     Please enter the correct username/password. \n""")
        # print(s.status_code)
    return session


def options(option, issue):
    return {
        '1': create_issues(issue)
    }.get(option, "0")


def get_issuetypes(json_createmeta):
    issue_types = json.loads(json_createmeta)
    num_projects = len(issue_types["projects"])
    metadata = []
    for i in range(0, num_projects):
        p_url = issue_types["projects"][i]['self']
        p_id = issue_types["projects"][i]['id']
        p_key = issue_types["projects"][i]['key']
        p_name = issue_types["projects"][i]['name']
        num_issues = len(issue_types["projects"][i]["issuetypes"])
        p_data = ProjectMeta(p_url, p_id, p_key, p_name)
        metadata.insert(i, p_data)
        # print(p_data)
        for x in range(0, num_issues):
            i_url = issue_types["projects"][i]['issuetypes'][x]['self']
            i_id = issue_types["projects"][i]['issuetypes'][x]['id']
            i_desc = issue_types["projects"][i]['issuetypes'][x]['description']
            i_name = issue_types["projects"][i]['issuetypes'][x]['name']
            task_metadata = IssueTypeMeta(i_url, i_id, i_desc, i_name)
            metadata[i].issuetype.append(task_metadata)
            # print(task_metadata)
    return metadata


def write_jira_key(issues, num_issues, filename):
    try:
        row_seed = 2
        wb = openpyxl.load_workbook('jira-import-template.xlsx')
        req_sheet = wb.get_sheet_by_name('Requirements')
        for issue_index in range(0, num_issues):
            issueKey = issues['issues'][issue_index]['key']
            req_sheet['F' + str(row_seed)] = issueKey
            val = constants.URL_BROWSE + issueKey
            req_sheet['F' + str(row_seed)].hyperlink = Hyperlink(ref="", target=val)
            req_sheet['F' + str(row_seed)].font = Font(color="006100")
            req_sheet['F' + str(row_seed)].fill = PatternFill("solid", fgColor="C6EFCE")
            # test.font = Font(color="#006100")
            # test.font = Font(color="#006100")
            # print('\n' + test.font)
            # req_sheet['F' + str(row_seed)].fill = Fill(fgColor="#C6EFCE")
            row_seed += 1
        wb.save(filename)
    except Exception:
        print("Please close the file, then try again.")

# def check_issue_completion():

# def scrub_doc cleans internal info to send dox to client

# def merge_docs merges clients and local


def form_query(issue):
    # issue.change_description  #description
    # issue.parent
    # issue.customer
    # issue.process
    # issue.platform
    summary = issue.process + ': ' + issue.change_type
    query = "project=" + issue.project_key + " and summary~'" \
            + summary + "' and description~'" + issue.change_description + "'"
    return query

# def for_queries(issue_list):
#     for issue in issue_list:
