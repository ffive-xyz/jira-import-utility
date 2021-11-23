from __future__ import annotations
from typing import Any, Dict, List, Type
import logging

import os
from dotenv import load_dotenv
from jira import JIRA
from jira.resources import Issue

load_dotenv()

logging.basicConfig(level=logging.INFO)


class Wbs_Issue:
    _issues: List[Wbs_Issue] = []
    jira_client = JIRA(os.getenv('server_url'), auth=(
        os.getenv('username'), os.getenv('password')))

    def __init__(self, summary: str, assigniee: str, pending_days: str) -> None:
        self.summary = summary
        self.assigniee = assigniee
        self.pending_days = pending_days
        if self._is_present():
            logging.info(f'Skipped: {self.summary}, issue already exists')
        else:
            self._issues.append(self)
            logging.info('Wbs_Issue created: ' + str(self))

    def __str__(self) -> str:
        return f'summary={self.summary}, assigniee={self.assigniee}, pending_days={self.pending_days}'

    def is_valid(self) -> bool:
        return self.summary != '' and self.assigniee != '' and self.pending_days != ''

    def get_fields(self) -> dict:
        if self.is_valid:
            return {
                'issuetype': {
                    "name": "Sub-task"
                },
                "summary": self.summary,
                'assignee': {
                    "name": self.assigniee
                },
                'timetracking': {
                    'originalEstimate': self.pending_days
                },
                'components': [{
                    "name": os.getenv('component_name')
                }],
                "project": {
                    "key": os.getenv('project_key')
                },
                "parent": {
                    "key": os.getenv('parent_issue_id')
                },
            }
        logging.error("Failed to create fields", self)
        raise ValueError("Cannot create fields, issue not valid")

    def _is_present(self) -> bool:
        try:
            sub_tasks: List[Issue] = self.jira_client.issue(
                os.getenv('parent_issue_id')).fields.subtasks
            summaries = [i.fields.summary for i in sub_tasks]
            return self.summary in summaries

        except Exception as e:
            logging.critical(e)
            return False

    @staticmethod
    def create_tickets() -> List[Dict[str, Any]]:
        all_issue_fields = [i.get_fields() for i in Wbs_Issue._issues]
        if len(all_issue_fields) > 0:
            all_issues = Wbs_Issue.jira_client.create_issues(all_issue_fields)
            logging.info('Created tickets')
            return all_issues

        logging.info('No tickets found')
        return []


def read_issue_from_csv(path: str):
    data = []
    with open(path, encoding='utf-8-sig') as f:
        data = f.readlines()

    for i in data:
        fields = [j.strip() for j in i.split(',')]
        Wbs_Issue(summary=fields[0],
                  assigniee=fields[1], pending_days=fields[2]+'d')


if __name__ == "__main__":
    read_issue_from_csv('import.csv')
    consent = input(
        "Are you sure to create following tickets? (Y|N): ").lower() == 'y'
    if consent:
        Wbs_Issue.create_tickets()
    else:
        logging.info("user aborted")
