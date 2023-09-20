import openai, finnhub, time, tweepy
from data import openAiSecret, finnhubSecret, twitterApi, twitterSecret, twitterAccess, twitterAccessSecret, twitterBearer

# Setup an openai Client
openai.api_key = openAiSecret

# Setup finnhub client
finnhub_client = finnhub.Client(api_key=finnhubSecret)

# Setup Twitter Client
client = tweepy.Client(bearer_token=twitterBearer, consumer_key=twitterApi,
    consumer_secret=twitterSecret,
    access_token=twitterAccess,
    access_token_secret=twitterAccessSecret)

# Needed Variables
ids = []
latestTweetId = None
# splittedTweets = completion["choices"][0]["message"]["content"].split("*")

def prompt(url, summary):
    global latestTweetId
    promptList = [f"Summarize the given cryptocurrency news in a tweet with less than 265 characters with two emojis at most. Here is the news: {summary}", f"Exemine the news' impact on related projects, and its effects in the short, medium, and long term in a tweet with less than 265 characters with two emojis at most. Here is the news: {summary}", f"Determine its outlook by rating its importance out of 10, rate industry impact out of 10, and whether it is bullish or bearish, or neutral, and rate out of 10 in a tweet with less than 265 characters with two emojis at most. Here is the news: {summary}"]
    #f"Explain the reason this news is important or not important, explain its industry impact and why would you rate it high impact or low impact in a tweet with less than 265 characters with two emojis at most. Here is the news: {summary}"
    for idx, promt in enumerate(promptList):
        if idx == 0:
            try:
                completion = openai.ChatCompletion.create(
                    model = "gpt-3.5-turbo",
                    messages = [{"role":"user", "content": promt}]
                )
                tweet = completion["choices"][0]["message"]["content"]
            except Exception as e:
                print(e)
                time.sleep(10)
                completion = openai.ChatCompletion.create(
                    model = "gpt-3.5-turbo",
                    messages = [{"role":"user", "content": promt}]
                )
                tweet = completion["choices"][0]["message"]["content"]
            while len(tweet) > 270:
                completion = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [{"role":"user", "content": promt}]
                )
                tweet = completion["choices"][0]["message"]["content"]
                print(tweet)
                time.sleep(5)
            print(tweet)
            while True:
                try:
                    tweeted = client.create_tweet(text=tweet)
                    break
                except Exception as e:
                    e = str(e)
                    if "You are not allowed to create a Tweet with duplicate content." in e:
                        print(e)
                        break
                    else:
                        print(e)
                        time.sleep(5)
                        try:
                            tweeted = client.create_tweet(text=tweet)
                            break
                        except Exception as e:
                            print(e)
                            break
            latestTweetId = tweeted.data["id"]
        else:
            try:
                completion = openai.ChatCompletion.create(
                    model = "gpt-3.5-turbo",
                    messages = [{"role":"user", "content": promt}]
                )
                tweet = completion["choices"][0]["message"]["content"]
            except Exception as e:
                print(e)
                time.sleep(10)
                completion = openai.ChatCompletion.create(
                    model = "gpt-3.5-turbo",
                    messages = [{"role":"user", "content": promt}]
                )
                tweet = completion["choices"][0]["message"]["content"]
            while len(tweet) > 270:
                completion = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [{"role":"user", "content": promt}]
                )
                tweet = completion["choices"][0]["message"]["content"]
                print(tweet)
                time.sleep(5)
            print(tweet)
            while True:
                try:
                    tweeted = client.create_tweet(text=tweet, in_reply_to_tweet_id=latestTweetId)
                    break
                except Exception as e:
                    e = str(e)
                    if "You are not allowed to create a Tweet with duplicate content." in e:
                        print(e)
                        break
                    else:
                        print(e)
                        time.sleep(5)
                        try:
                            tweeted = client.create_tweet(text=tweet)
                            break
                        except Exception as e:
                            print(e)
                            break
            latestTweetId = tweeted.data["id"]
        time.sleep(5)
    time.sleep(5)
    while True:
        try:
            tweeted = client.create_tweet(text=url, in_reply_to_tweet_id=latestTweetId)
            break
        except Exception as e:
            e = str(e)
            if "You are not allowed to create a Tweet with duplicate content." in e:
                print(e)
                break
            else:
                print(e)
                time.sleep(5)
                try:
                    tweeted = client.create_tweet(text=tweet)
                    break
                except Exception as e:
                    print(e)
                    break
while True:
    ids = ids[-250:]
    # Get the most recently tweeted news
    with open('lastId.txt') as f:
        text = f.readlines()
    if text:
        lastId = int(text[0])
        print(lastId)
    else: 
        lastId = 0
    while True:
        try:
            response = finnhub_client.general_news('crypto', min_id=lastId)
            break
        except Exception as e:
            print(e)
            time.sleep(5)
    print(response)
    for data in response:
        if data["id"] not in ids:
            ids.append(data["id"])
            newsSummary = data["summary"]
            newsUrl = data["url"]
            try:
                prompt(newsUrl, newsSummary)
            except Exception as e:
                print(e)
                pass
            if ids: 
                with open('lastId.txt', 'w') as f:
                    f.write(f"{max(ids)}")
                    print(max(ids))
        else:
            pass
        time.sleep(5)
    time.sleep(600)
        

