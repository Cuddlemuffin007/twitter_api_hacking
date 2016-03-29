import random
from profanity import profanity
from TwitterAPI import TwitterAPI


consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''

profanity.set_censor_characters('💩')
search_terms = profanity.get_words()

api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

r = api.request('search/tweets', {'q': random.choice(search_terms), 'lang': 'en'})

for tweet in r:
    tweet_text = tweet.get('text')
    tweet_poster = tweet.get('user').get('screen_name')
    tweet_id = tweet.get('id')
    if 'RT' not in tweet_text.split()[0] and len(tweet_text) < (133 - len(tweet_poster)):
        if profanity.contains_profanity(tweet_text):

            # tweet at the user with their corrected tweet
            censorship_tweet = api.request(
                    'statuses/update', {
                        'status': "{}*ftfy @{}".format(profanity.censor(tweet_text), tweet_poster),
                        'in_reply_to_status_id': int(tweet_id)
                        }
            )
            print('Censored: {}'.format(censorship_tweet.status_code))

            # like the tweet
            like = api.request('favorites/create', {'id': int(tweet_id)})
            print('Like: {}'.format(like.status_code))

            # follow the user
            follow = api.request('friendships/create', {'screen_name': tweet_poster})
            print('Follow: {}'.format(follow.status_code))

            # mute the user
            mute = api.request('mutes/users/create', {'screen_name': tweet_poster})
            print('Mute: {}'.format(mute.status_code))
        else:
            print('No profanity found. Good job Twitter!')
else:
    print('No tweets found to edit.')
