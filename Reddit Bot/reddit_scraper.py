import praw
import pandas as pd
import datetime
import matplotlib.pyplot as plt

reddit = praw.Reddit(
    client_id="my client id",
    client_secret="my client secret",
    user_agent="my user agent"
)

def create_dataframe_from_data():
    df = pd.DataFrame(generate_subreddit_data())
    generate_csv(df)
    print(df.sort_values("Score", ascending=False, ignore_index=True).head(10))

def generate_subreddit_data():
    subreddit_gaming = reddit.subreddit("gaming")

    scraped_posts = list()
    for submission in subreddit_gaming.top(time_filter="all", limit=300):
        subreddit = submission.subreddit
        title = submission.title
        score = submission.score
        upvote_ratio = submission.upvote_ratio
        created = submission.created_utc
        nsfw = submission.over_18
        data_set = {"Subreddit": subreddit, "Title": title, "Score": score, "Upvote Ratio": upvote_ratio, "Created": datetime.datetime.fromtimestamp(created), "NSFW": nsfw}
        scraped_posts.append(data_set)

    return scraped_posts

def generate_csv(df):
    df.to_csv('data.csv', sep=',', index=False)

create_dataframe_from_data()
