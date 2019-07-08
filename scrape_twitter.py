#!/usr/bin/python3
import twint
import datetime

# Determine today's date
today = datetime.date.today()
# Format Twitter hashtag (based on current day).
twitterHashTag = '#' + today.strftime("%A").lower() + 'thoughts'

# Configure Twint to search for the above hashtag
# We only want text-only results for the current date (limit 60).
c = twint.Config()
c.Search = twitterHashTag
c.Limit = 60
c.Store_json = True
c.Custom["tweet"] = ["id", "date", "username", "created_at", "tweet"]
c.User_full = True
c.Output = "tweets.json"
c.Format = "Tweet id: {id} | Date: {date} | Tweet: {tweet}"

# Run
twint.run.Search(c)