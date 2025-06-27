import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")  # e.g. https://your-domain.atlassian.net
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")  # e.g. "PROJ"

AUTH = (EMAIL, API_TOKEN)
HEADERS = {"Accept": "application/json"}

def fetch_all_issues():
    start_at = 0
    max_results = 100
    all_issues = []

    while True:
        url = f"{JIRA_BASE_URL}/rest/api/3/search"
        params = {
            "jql": f"project={PROJECT_KEY}",
            "startAt": start_at,
            "maxResults": max_results
        }
        response = requests.get(url, headers=HEADERS, params=params, auth=AUTH)
        data = response.json()

        issues = data.get("issues", [])
        if not issues:
            break

        for issue in issues:
            fields = issue.get("fields", {})
            all_issues.append({
                "key": issue.get("key"),
                "summary": fields.get("summary", ""),
                "description": fields.get("description", {}).get("content", "") if isinstance(fields.get("description"), dict) else fields.get("description", "")
            })

        start_at += max_results

    with open("all_jira_issues.json", "w", encoding="utf-8") as f:
        json.dump(all_issues, f, indent=2, ensure_ascii=False)

    print(f"✅ Exported {len(all_issues)} Jira issues.")

if __name__ == "__main__":
    fetch_all_issues()
