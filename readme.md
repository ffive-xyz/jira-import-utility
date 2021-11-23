# JIRA Import Utility

This utility imports csv file to jira.
CSV file should be exported from excel.

👉 **Make sure `import.csv` should have encoding of `utf-8 with BOM`**

## How to use
- Create `.env` file. (Use `.env.template` for reference)
- Create `import.csv` file. (Use `import.template.csv` for reference)
- install dependencies `pip install -r requirements.txt`
- run script using `python main.py`

## Features
- Ability to create JIRA subtasks from csv
- Check for duplicate subtask before creation

Feel free to modify and use. If you have any suggestions, then do create an issue/PR.
