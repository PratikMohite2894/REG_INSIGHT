import json
import os

def load_jira_issues(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_confluence_pages(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def combine_data(jira_path, confluence_path):
    jira_data = load_jira_issues(jira_path)
    confluence_data = load_confluence_pages(confluence_path)

    combined = []

    for issue in jira_data:
        combined.append({
            "source": "jira",
            "title": issue.get("summary"),
            "content": issue.get("description", "")
        })

    for page in confluence_data:
        combined.append({
            "source": "confluence",
            "title": page.get("title"),
            "content": page.get("content", "")
        })

    return combined