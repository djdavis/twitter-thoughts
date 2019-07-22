#!/usr/bin/python3
import twint
from datetime import datetime
import re
import json
import boto3

# AWS S3
s3 = boto3.resource('s3')
bucketName = 'tweet-captures'
keyName = 'tweets.json'
# Determine the day of the week
today = datetime.today().strftime('%A').lower()
# Format Twitter hashtag based on current day (ex. #{day}thoughts).
twitterHashTag = f'#{today}thoughts'


def search_for_tweets_by_hash_tag():
    # Configure Twint to search for the hashtag
    c = twint.Config()
    c.Search = twitterHashTag
    c.Limit = 60
    c.Custom["tweet"] = ["id", "date", "username", "created_at", "tweet"]
    c.User_full = False
    c.Format = "Tweet id: {id} | Date: {date} | Tweet: {tweet}"
    c.Store_object = True
    c.Hide_output = True
    twint.run.Search(c)
    if len(twint.output.tweets_object) > 0:
        return twint.output.tweets_object
    else:
        return False


def clean_tweets(tweets):
    output = []
    for tweet in tweets:
        output.append({'author': tweet.username, 'tweet': clean_tweet(tweet.tweet)})

    return output


def clean_tweet(tweet):
    tweet = re.sub('http\S+', '', tweet)  # remove URLs
    tweet = re.sub('pic.\S+', '', tweet)  # remove URLs
    tweet = re.sub('RT|cc', '', tweet)  # remove RT and cc
    tweet = re.sub('#\S+', '', tweet)  # remove hashtags
    tweet = re.sub('@\S+', '', tweet)  # remove mentions
    tweet = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), '', tweet)  # remove punctuations
    tweet = re.sub('\s+', ' ', tweet)  # remove extra whitespace
    tweet = tweet.encode('ascii', 'ignore').decode('ascii')
    return tweet


def store_in_s3(tweets):
    # Convert the tweets to JSON, then send to S3
    s3object = s3.Object(bucketName, keyName)
    s3object.put(
        Body=(bytes(json.dumps(tweets).encode('UTF-8')))
    )
    # Make sure it exists
    uploaded_file = s3.head_object(bucketName, keyName)
    if uploaded_file['ContentLength'] > 0:
        return True
    else:
        raise Exception('Failed to store file in S3')


def main(event, context):
    """Main handler for the lambda function.  """
    # Try/except everything
    try:
        # Attempt to retrieve Tweets and temporarily store
        results = search_for_tweets_by_hash_tag()
        if results != False:
            # If we were able to find tweets, lets clean them
            cleansed_tweets = clean_tweets(results)
            # Now lets store them in AWS S3
            store_in_s3(cleansed_tweets)
        else:
            raise Exception('Failed to retrieve tweets!')
    except BaseException as exception:
        # Catch everything and log the event that failed
        print(exception)

        # Re-raise the exception so lambda can handle this as an unsuccessful attempt and the event can be re-tried
        raise exception


# Debug
#event = 'test'
#context = 'test'
#main(event, context)