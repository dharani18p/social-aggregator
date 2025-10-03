import requests
from config import GITHUB_API_URL, GITHUB_TOKEN

headers = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_top_issues_by_comments(owner, repo):
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues?state=open&per_page=100"
    response = requests.get(url, headers=headers).json()
    issues = sorted(response, key=lambda x: x.get("comments", 0), reverse=True)
    return issues[:5]

def get_author_with_most_issues(owner, repo):
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues?state=open&per_page=100"
    response = requests.get(url, headers=headers).json()
    author_count = {}
    for issue in response:
        author = issue["user"]["login"]
        author_count[author] = author_count.get(author, 0) + 1
    return max(author_count, key=author_count.get), author_count

def get_repo_with_most_open_issues(org, repos):
    max_repo, max_count = None, 0
    for repo in repos:
        url = f"{GITHUB_API_URL}/repos/{org}/{repo}"
        response = requests.get(url, headers=headers).json()
        open_count = response.get("open_issues_count", 0)
        if open_count > max_count:
            max_repo, max_count = repo, open_count
    return max_repo, max_count
