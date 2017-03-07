from Issue import Issue
import openpyxl
from JiraApi import jira_create_issues, create_issue, get_issue, search_issues
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
ISSUE_TYPE = "10102"
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


""" =========================================================================
|                           Accessor Methods                                |
=========================================================================="""


def get_change_type(req_sheet, row_num):
    """ Accessor for Change Type
    Args:
        req_sheet: A variable holding an Excel Workbook sheet in memory.
        row_num: A variable holding the row # of the data being accessed.
    Returns:
            A string value of the Change Type
"""
    return (req_sheet['A' + str(row_num)].value)


def get_change_description(req_sheet, row_num):
    """ Accessor for Change Description
    Args:
        req_sheet: A variable holding an Excel Workbook sheet in memory.
        row_num: A variable holding the row # of the data being accessed.
    Returns:
            A string value of the Change Description
    """
    return (req_sheet['B' + str(row_num)].value)


def get_platform(req_sheet, row_num):
    """ Accessor for Platform
    Args:
        req_sheet: A variable holding an Excel Workbook sheet in memory.
        row_num: A variable holding the row # of the data being accessed.
    Returns:
            A string value of the Platform
"""
    return (req_sheet['C' + str(row_num)].value)


def get_process(req_sheet, row_num):
    """ Accessor for Process
    Args:
        req_sheet: A variable holding an Excel Workbook sheet in memory.
        row_num: A variable holding the row # of the data being accessed.
    Returns:
            A string value of the Process
    """
    return (req_sheet['D' + str(row_num)].value)


def get_notes(req_sheet, row_num):
    """ Accessor for Notes
    Args:
        req_sheet: A variable holding an Excel Workbook sheet in memory.
        row_num: A variable holding the row # of the data being accessed.
    Returns:
            A string value of the Notes
    """
    return (req_sheet['E' + str(row_num)].value)


def get_jira_task(req_sheet, row_num):
    """ Accessor for JIRA Key
    Args:
        req_sheet: A variable holding an Excel Workbook sheet in memory.
        row_num: A variable holding the row # of the data being accessed.
    Returns:
            A string value of the Notes
    """
    return (req_sheet['F' + str(row_num)].value)


def get_status(req_sheet, row_num):
    """ Accessor for JIRA Key
    Args:
        req_sheet: A variable holding an Excel Workbook sheet in memory.
        row_num: A variable holding the row # of the data being accessed.
    Returns:
            A string value of the Notes
    """
    return (req_sheet['G' + str(row_num)].value)


def get_assign_to(req_sheet, row_num):
    """ Accessor for Assign To field
    Args:
        req_sheet: A variable holding an Excel Workbook sheet in memory.
        row_num: A variable holding the row # of the data being accessed.
    Returns:
            A string value of the Notes
    """
    return (req_sheet['H' + str(row_num)].value)


def get_customer(customer_sheet):
    """ Accessor for Customer

    Args:
        customer_sheet: A variable holding an Excel Workbook sheet in memory.
    Returns:
            A string value of the Customer
    """
    return (customer_sheet['A' + "2"].value)


def get_parent(jira_sheet, process):
    """ Accessor for Parent

    Accessor method for retrieving the value for Parent (JIRA Key) on the
    JIRA Stories Sheet.

    There is a check to make certain the process in question is amongst those
    qualified to exist.

    Args:
        jira_sheet: A variable holding an Excel Workbook sheet in memory.
        process: A variable holding the process of an Issue.
    Returns:
            A string value of the Parent
"""
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


""" =========================================================================
|                          End Accessor Methods                            |
=========================================================================="""


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
                    # print(issue)
                    # print(issue.text)
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
    """ Reads Excel Workbook into memory

    Args:
        filename: A variable holding the document's filename

    """
    try:
        if filename is None:
            filename = input("Please enter a filename: ")
        wb = openpyxl.load_workbook(filename=filename)
        return wb
    except Exception:
        print("Invalid file name\n")


def parseFile(wb, session=None, filename=None):
    """ Parses Workbook into Issues Objects

        Iterates through each row containing data within the Workbook
        while creating an Issue object capturing all of the information.

        A Story ( Parent ) is required in order to create Sub-tasks ( info on Requirements sheet)
        therefore there is a check prior to processing the file in place in order to create
        a Story ( Parent ) if they don't already exist.

    Args:
        wb: A variable holding a Excel Workbook in memory.
        session: An optional variable holding the current Session.
        filename: An optional variable holding the filename of the Workbook
    Return: A list of Issue Objects
    """
    try:
        req_sheet = wb.get_sheet_by_name('Requirements')
        jira_sheet = wb.get_sheet_by_name('JIRA Stories')
        customer_sheet = wb.get_sheet_by_name('Customer Info')
        issues = []
        maxRow = req_sheet.max_row
        customer = get_customer(customer_sheet)

        # Determines if Stories have already been created for each Sub-task
        stories = get_stories(jira_sheet, customer_sheet)
        create_stories(stories, session, wb, filename)

        #  Process File
        for row in range(2, maxRow + 1):
            issue = Issue()
            issue.change_type = get_change_type(req_sheet, row)
            issue.change_description = get_change_description(req_sheet, row)
            issue.platform = str(get_platform(req_sheet, row))
            issue.process = str(get_process(req_sheet, row))
            issue.notes = get_notes(req_sheet, row)
            issue.parent = get_parent(jira_sheet, issue.process)
            issue.customer = customer
            issue.issue_type = ISSUE_TYPE
            issue.project_key = PROJECT_KEY
            issue.jira_key = get_jira_task(req_sheet, row)
            issue.row = str(row)
            issues.append(issue)
        return issues
    except Exception:
        print("Error processing file.")


def login():
    """ Method for logging into JIRA and capturing Session
        Args: None
        Return: Session
    """
    authenticated = False
    while authenticated is not True:
        # username = input("Please enter your JIRA username: ")
        # password = getpass.getpass("Please enter your JIRA password: ")
        username = "admin"
        password = "admin"
        session = requests.Session()
        cred = json.dumps({"username": username, "password": password})
        s = session.post(constants.URI_LOGIN,
                         headers=constants.APPLICATION_JSON,
                         data=cred)
        authenticated = s.ok
        if (not s.ok):
            print("\nInvalid login credentials. \
                    Please enter the correct username/password. \n")
        # print(s.status_code)
    return session


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


def write_jira_key(issues, filename):
    try:
        wb = openpyxl.load_workbook(filename)
        req_sheet = wb.get_sheet_by_name('Requirements')
        for issue in issues:
            req_sheet['F' + str(issue.row)] = issue.jira_key
            val = constants.URL_BROWSE + issue.jira_key
            req_sheet['F' + str(issue.row)].hyperlink = Hyperlink(ref="",
                                                                  target=val)
        wb.save(filename)
    except Exception:
        print("Error: Write Jira Key - Please close the file, then try again.")


def update_status(issue_list, session, filename):
    try:
        row_seed = 2
        wb = openpyxl.load_workbook('jira-import-template.xlsx')
        req_sheet = wb.get_sheet_by_name('Requirements')
        for issue in issue_list:
            issueStatusJson = get_issue(issue.jira_key, session)
            issueStatus = json.loads(issueStatusJson.text)
            issueStatus = issueStatus['fields']['status']['name']
            req_sheet['G' + str(row_seed)] = issueStatus
            done = PatternFill("solid", fgColor="C6EFCE")
            todo = PatternFill("solid", fgColor="FFC7CE")
            in_progress = PatternFill("solid", fgColor="FFEB9C")
            if issueStatus == "To Do":
                req_sheet['A' + str(row_seed)].fill = todo
                req_sheet['B' + str(row_seed)].fill = todo
                req_sheet['C' + str(row_seed)].fill = todo
                req_sheet['D' + str(row_seed)].fill = todo
                req_sheet['E' + str(row_seed)].fill = todo
                req_sheet['F' + str(row_seed)].fill = todo
                req_sheet['G' + str(row_seed)].fill = todo
            elif issueStatus == "Done":
                req_sheet['B' + str(row_seed)].fill = done
                req_sheet['A' + str(row_seed)].fill = done
                req_sheet['C' + str(row_seed)].fill = done
                req_sheet['D' + str(row_seed)].fill = done
                req_sheet['E' + str(row_seed)].fill = done
                req_sheet['F' + str(row_seed)].fill = done
                req_sheet['G' + str(row_seed)].fill = done
            else:
                req_sheet['A' + str(row_seed)].fill = in_progress
                req_sheet['B' + str(row_seed)].fill = in_progress
                req_sheet['C' + str(row_seed)].fill = in_progress
                req_sheet['D' + str(row_seed)].fill = in_progress
                req_sheet['E' + str(row_seed)].fill = in_progress
                req_sheet['F' + str(row_seed)].fill = in_progress
                req_sheet['G' + str(row_seed)].fill = in_progress
            row_seed += 1
        wb.save(filename)
    except Exception:
        print("Please close the file, then try again.")


# def scrub_doc cleans internal info to send dox to client

# def merge_docs merges clients and local


def form_query(issue):
    summary = issue.process + ': ' + issue.change_type
    query = "project=" + issue.project_key + " and summary~'" \
            + summary + "' and description~'" + issue.change_description + "'"
    return query


def write_status(issues, filename, session):
    try:
        wb = openpyxl.load_workbook(filename)
        req_sheet = wb.get_sheet_by_name('Requirements')
        for issue in issues:
            req_sheet['G' + issue.row] = issue.status
            done = PatternFill("solid", fgColor="C6EFCE")
            todo = PatternFill("solid", fgColor="FFC7CE")
            in_progress = PatternFill("solid", fgColor="FFEB9C")
            if issue.status == "To Do":
                req_sheet['A' + issue.row].fill = todo
                req_sheet['B' + issue.row].fill = todo
                req_sheet['C' + issue.row].fill = todo
                req_sheet['D' + issue.row].fill = todo
                req_sheet['E' + issue.row].fill = todo
                req_sheet['F' + issue.row].fill = todo
                req_sheet['G' + issue.row].fill = todo
            elif issue.status == "Done":
                req_sheet['B' + issue.row].fill = done
                req_sheet['A' + issue.row].fill = done
                req_sheet['C' + issue.row].fill = done
                req_sheet['D' + issue.row].fill = done
                req_sheet['E' + issue.row].fill = done
                req_sheet['F' + issue.row].fill = done
                req_sheet['G' + issue.row].fill = done
            else:
                req_sheet['A' + issue.row].fill = in_progress
                req_sheet['B' + issue.row].fill = in_progress
                req_sheet['C' + issue.row].fill = in_progress
                req_sheet['D' + issue.row].fill = in_progress
                req_sheet['E' + issue.row].fill = in_progress
                req_sheet['F' + issue.row].fill = in_progress
                req_sheet['G' + issue.row].fill = in_progress
        wb.save(filename)
    except Exception:
        print("Please close the file, then try again.")

# def for_queries(issue_list):
#     for issue in issue_list:


def create_issues(session, issues, filename):
    # non_created_issues = [(issue for issue in Issues
    #                        if not is_issue_created(issue))]
    # for issue in non_created_issues:
    #     print(issue)
    try:
        non_created_issues = []
        for issue in issues:
            duplicate = is_duplicate(issue, session)
            if not issue.jira_key and not duplicate:
                non_created_issues.append(issue)
        if non_created_issues:
            json_issue_response = jira_create_issues(session,
                                                     non_created_issues)
            i = 0
            for pending_issue in non_created_issues:
                issue_reponse = json.loads(json_issue_response.text)
                pending_issue.jira_key = issue_reponse['issues'][i]['key']
                print(pending_issue.jira_key)
                issueStatusJson = get_issue(pending_issue.jira_key, session)
                issueStatus = json.loads(issueStatusJson.text)
                pending_issue.status = issueStatus['fields']['status']['name']
                i = i + 1
            write_jira_key(non_created_issues, filename)
            write_status(non_created_issues, filename, session)
        else:
            return print("Nothing to update!")
    except Exception:
        print("Error: Create_Issues")


def is_issue_created(issue, s):
    return True if issue.jira_key else False


def is_duplicate(issue, session):
    search_query = form_query(issue)
    field_list = []
    field_list.append("summary, status")
    search = json.loads(search_issues(search_query,field_list=field_list, session=session).text)
    return True if search['total'] else False
