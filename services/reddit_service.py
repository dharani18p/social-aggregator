import praw
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def get_top_posts(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.top(limit=5):
        posts.append({"title": post.title, "author": str(post.author), "upvotes": post.score})
    return posts

def get_top_author_by_upvotes(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    author_scores = {}
    for post in subreddit.top(limit=50):
        author = str(post.author)
        author_scores[author] = author_scores.get(author, 0) + post.score
    top_author = max(author_scores, key=author_scores.get)
    return {"author": top_author, "total_upvotes": author_scores[top_author]}
