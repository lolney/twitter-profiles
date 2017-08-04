import twitter, os

def GetConsumerKeyEnv():
    return os.environ.get("TWEETUSERNAME", None)

def GetConsumerSecretEnv():
    return os.environ.get("TWEETPASSWORD", None)

def GetAccessKeyEnv():
    return os.environ.get("TWEETACCESSKEY", None)

def GetAccessSecretEnv():
    return os.environ.get("TWEETACCESSSECRET", None)

def get_statuses(user):
    api = twitter.Api(consumer_key=GetConsumerKeyEnv(), consumer_secret=GetConsumerSecretEnv(),
                      access_token_key=GetAccessKeyEnv(), access_token_secret=GetAccessSecretEnv())
    statuses = api.GetUserTimeline(user)
    return statuses