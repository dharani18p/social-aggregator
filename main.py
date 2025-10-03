from flask import Flask, jsonify, request, render_template
import requests
import os

app = Flask(__name__)

# Get token from environment variable or use placeholder
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "YOUR_GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"

github_headers = {
    "Accept": "application/vnd.github.v3+json",
}

# Only add authorization if token is set
if GITHUB_TOKEN and GITHUB_TOKEN != "YOUR_GITHUB_TOKEN":
    github_headers["Authorization"] = f"token {GITHUB_TOKEN}"

# ---------------- GitHub Functions ----------------
def get_top_issues_by_comments(owner, repo):
    """Fetch top 5 issues by comment count"""
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues?state=open&sort=comments&direction=desc&per_page=5"
    print(f"Fetching: {url}")  # Debug print
    response = requests.get(url, headers=github_headers)
    print(f"Status: {response.status_code}")  # Debug print
    response.raise_for_status()
    issues = response.json()
    
    # Filter out pull requests (they also appear in issues endpoint)
    issues = [i for i in issues if 'pull_request' not in i]
    
    return [
        {
            "title": i["title"], 
            "comments": i["comments"], 
            "url": i["html_url"]
        }
        for i in issues[:5]
    ]

def get_author_with_most_issues(owner, repo):
    """Find author with most open issues"""
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues?state=open&per_page=100"
    print(f"Fetching: {url}")  # Debug print
    response = requests.get(url, headers=github_headers)
    response.raise_for_status()
    issues = response.json()
    
    # Filter out pull requests
    issues = [i for i in issues if 'pull_request' not in i]
    
    author_count = {}
    for issue in issues:
        author = issue["user"]["login"]
        author_count[author] = author_count.get(author, 0) + 1
    
    if not author_count:
        return None, 0
    
    top_author = max(author_count, key=author_count.get)
    return top_author, author_count[top_author]

def get_repo_with_most_open_issues(owner, repos):
    """Find repo with most open issues from a list"""
    max_repo, max_count = None, -1
    for repo in repos:
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"
        print(f"Fetching: {url}")  # Debug print
        r = requests.get(url, headers=github_headers)
        if r.status_code != 200:
            print(f"Failed to fetch {repo}: {r.status_code}")
            continue
        data = r.json()
        open_issues = data.get("open_issues_count", 0)
        print(f"{repo}: {open_issues} open issues")
        if open_issues > max_count:
            max_count = open_issues
            max_repo = repo
    return max_repo, max_count

# ---------------- Reddit Functions ----------------
def get_top_reddit_posts(subreddit, limit=5):
    """Fetch top Reddit posts by upvotes"""
    url = f"https://www.reddit.com/r/{subreddit}/top.json?limit={limit}&t=day"
    headers = {"User-Agent": "social-aggregator/0.1"}
    print(f"Fetching: {url}")  # Debug print
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    posts = r.json()["data"]["children"]
    return [
        {
            "title": p["data"]["title"], 
            "upvotes": p["data"]["ups"], 
            "author": p["data"]["author"]
        }
        for p in posts
    ]

def get_reddit_author_with_most_posts(subreddit):
    """Find Reddit author with most posts"""
    url = f"https://www.reddit.com/r/{subreddit}/top.json?limit=100&t=day"
    headers = {"User-Agent": "social-aggregator/0.1"}
    print(f"Fetching: {url}")  # Debug print
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    posts = r.json()["data"]["children"]
    authors = {}
    for p in posts:
        author = p["data"]["author"]
        authors[author] = authors.get(author, 0) + 1
    
    if not authors:
        return {"author": "N/A", "posts": 0}
    
    top_author = max(authors, key=authors.get)
    return {"author": top_author, "posts": authors[top_author]}

# ---------------- Flask Routes ----------------
@app.route("/")
def index():
    return render_template("index.html")

# GitHub API routes
@app.route("/api/github/top-issues")
def github_top_issues():
    owner = request.args.get("owner")
    repo = request.args.get("repo")
    
    if not owner or not repo:
        return jsonify({"error": "Owner and repo required"}), 400
    
    try:
        issues = get_top_issues_by_comments(owner, repo)
        return jsonify(issues)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return jsonify({"error": "Repository not found"}), 404
        elif e.response.status_code == 403:
            return jsonify({"error": "API rate limit exceeded. Please add a GitHub token."}), 403
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 500

@app.route("/api/github/top-author")
def github_top_author():
    owner = request.args.get("owner")
    repo = request.args.get("repo")
    
    if not owner or not repo:
        return jsonify({"error": "Owner and repo required"}), 400
    
    try:
        author, count = get_author_with_most_issues(owner, repo)
        if author is None:
            return jsonify({"author": "N/A", "issue_count": 0})
        return jsonify({"author": author, "issue_count": count})
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return jsonify({"error": "Repository not found"}), 404
        elif e.response.status_code == 403:
            return jsonify({"error": "API rate limit exceeded. Please add a GitHub token."}), 403
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 500

@app.route("/api/github/top-repo")
def github_top_repo():
    owner = request.args.get("owner")
    repos_str = request.args.get("repos")
    
    if not owner or not repos_str:
        return jsonify({"error": "Owner and repos required"}), 400
    
    repos = [r.strip() for r in repos_str.split(",")]
    
    try:
        repo, count = get_repo_with_most_open_issues(owner, repos)
        if repo is None:
            return jsonify({"error": "No valid repositories found"}), 404
        return jsonify({"repo": repo, "open_issues": count})
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            return jsonify({"error": "API rate limit exceeded. Please add a GitHub token."}), 403
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 500

# Reddit API routes
@app.route("/api/reddit/top-posts")
def reddit_top_posts():
    subreddit = request.args.get("subreddit")
    
    if not subreddit:
        return jsonify({"error": "Subreddit required"}), 400
    
    try:
        posts = get_top_reddit_posts(subreddit)
        return jsonify(posts)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return jsonify({"error": "Subreddit not found"}), 404
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 500

@app.route("/api/reddit/top-author")
def reddit_top_author():
    subreddit = request.args.get("subreddit")
    
    if not subreddit:
        return jsonify({"error": "Subreddit required"}), 400
    
    try:
        result = get_reddit_author_with_most_posts(subreddit)
        return jsonify(result)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return jsonify({"error": "Subreddit not found"}), 404
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 500

# ---------------- Run ----------------
if __name__ == "__main__":
    print("Starting Social Media Aggregator...")
    print(f"GitHub token configured: {GITHUB_TOKEN != 'YOUR_GITHUB_TOKEN'}")
    app.run(debug=True, port=5000)