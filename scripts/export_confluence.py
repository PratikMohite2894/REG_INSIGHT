import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")  # e.g. https://your-domain.atlassian.net/wiki
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")  # e.g. "PROJECT"

AUTH = (EMAIL, API_TOKEN)
HEADERS = {"Accept": "application/json"}

def fetch_all_pages():
    start = 0
    limit = 50
    all_pages = []

    while True:
        url = f"{CONFLUENCE_BASE_URL}/rest/api/content"
        params = {
            "spaceKey": SPACE_KEY,
            "limit": limit,
            "start": start,
            "expand": "body.storage"
        }

        response = requests.get(url, headers=HEADERS, auth=AUTH, params=params)
        data = response.json()

        results = data.get("results", [])
        if not results:
            break

        for page in results:
            all_pages.append({
                "id": page["id"],
                "title": page["title"],
                "content": page["body"]["storage"]["value"]
            })

        if "_links" in data and "next" in data["_links"]:
            start += limit
        else:
            break

    with open("all_confluence_pages.json", "w", encoding="utf-8") as f:
        json.dump(all_pages, f, indent=2, ensure_ascii=False)

    print(f"✅ Exported {len(all_pages)} Confluence pages.")

if __name__ == "__main__":
    fetch_all_pages()

