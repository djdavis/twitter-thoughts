#!/usr/bin/python3
import twint
import datetime

# Determine today's date
today = datetime.date.today()
# Format Twitter hashtag (based on current day).
twitterHashTag = '#' + today.strftime("%A").lower() + 'thoughts'


def search_for_tweets_by_hash_tag(hashtag):
    # Configure Twint to search for the above hashtag
    # We only want text-only results for the current date (limit 60).
    c = twint.Config()
    c.Search = hashtag
    c.Limit = 60
    c.Store_json = True
    c.Custom["tweet"] = ["id", "date", "username", "created_at", "tweet"]
    c.User_full = True
    c.Output = "tweets.json"
    c.Format = "Tweet id: {id} | Date: {date} | Tweet: {tweet}"
    twint.run.Search(c)


search_for_tweets_by_hash_tag(twitterHashTag)

