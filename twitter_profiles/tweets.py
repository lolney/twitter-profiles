import twitter, os

def GetConsumerKeyEnv():
    return os.environ.get("TWEETUSERNAME", None)

def GetConsumerSecretEnv():
    return os.environ.get("TWEETPASSWORD", None)

def GetAccessKeyEnv():
    return os.environ.get("TWEETACCESSKEY", None)

def GetAccessSecretEnv():
    return os.environ.get("TWEETACCESSSECRET", None)

def get_statuses(user=None, screen_name=None):
    api = twitter.Api(consumer_key=GetConsumerKeyEnv(), consumer_secret=GetConsumerSecretEnv(),
                      access_token_key=GetAccessKeyEnv(), access_token_secret=GetAccessSecretEnv())
    statuses = []
    if user is not None:
        statuses = api.GetUserTimeline(user)
    elif screen_name is not None:
        statuses = api.GetUserTimeline(screen_name=screen_name)
    else:
        raise ValueError("Must provide either user or screen_name")
    return statuses