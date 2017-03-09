import utilities

filename = "jira-import-template.xlsx"
s = utilities.login()
wb = utilities.readFile(filename)
issues = utilities.parseFile(wb, session=s, filename=filename)
utilities.update_status(issues, s, filename)
