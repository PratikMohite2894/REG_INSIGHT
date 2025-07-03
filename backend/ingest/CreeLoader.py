import json
import os

def load_cree_jira_issues(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_cree_confluence_pages(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def combine_cree_data(jira_path, confluence_path):
    jira_data = load_cree_jira_issues(jira_path)
    confluence_data = load_cree_confluence_pages(confluence_path)

    flat_confluence_data = []
    combined = []

    # Combine Jira data
    for issue in jira_data:
        combined.append({
            "source": "jira",
            "jira_id": issue.get("jira_id", ""),
            "title": issue.get("summary", ""),
            "description": issue.get("description", ""),
            "created_date": issue.get("created_date", ""),
            "updated_date": issue.get("updated_date", ""),
            "status": issue.get("status", ""),
            "assignee": issue.get("assignee", ""),
            "reporter": issue.get("reporter", ""),
            "priority": issue.get("priority", ""),
            "eta": issue.get("eta", "")
        })

    # Flatten confluence data if needed
    for item in confluence_data:
        if isinstance(item, list):
            flat_confluence_data.extend(item)
        else:
            flat_confluence_data.append(item)

    # Combine confluence data
    for page in flat_confluence_data:
        combined.append({
            "source": "confluence",
            "confluence_id": page.get("confluence_id", ""),
            "title": page.get("title", ""),
            "created_time": page.get("created_time", ""),
            "created_by": page.get("created_by", ""),
            "description": page.get("description", ""),
            "acceptance_criteria": ", ".join(page.get("acceptance_criteria", []))
        })

    return combined
