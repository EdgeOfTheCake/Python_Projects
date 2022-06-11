Type in the console to install the required packeges:
    - pip install -r requirements.txt

In this project I've created two small reddit bots.
The reddit_bot.py is replying on posts and comments in the subreddit "FunnyAnimals/technology".
The reddit_scraper.py is scraping the subreddit "gaming" and creates a DataFrame from the data scraped.

You can use my code if you want, but first you have to create a reddit profile for yourself at https://www.reddit.com/
Also you have to create an app at https://www.reddit.com/prefs/apps and replace "reddit = praw.Reddit..." items with yours.
If you need any help you can find how reddit bots works in the documentation: https://praw.readthedocs.io/en/stable/getting_started/quick_start.html

Room for improvement:
    - Better error handeling for eg. not using sleep for reaching reddit time limit.