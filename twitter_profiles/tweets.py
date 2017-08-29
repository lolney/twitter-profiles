import twitter, os

def GetConsumerKeyEnv():
    return os.environ.get("TWEETUSERNAME", None)

def GetConsumerSecretEnv():
    return os.environ.get("TWEETPASSWORD", None)

def GetAccessKeyEnv():
    return os.environ.get("TWEETACCESSKEY", None)

def GetAccessSecretEnv():
    return os.environ.get("TWEETACCESSSECRET", None)

class TwitterAPI:

    def __init__(self):
        self.api = twitter.Api(consumer_key=GetConsumerKeyEnv(), consumer_secret=GetConsumerSecretEnv(),
                      access_token_key=GetAccessKeyEnv(), access_token_secret=GetAccessSecretEnv())

    def get_statuses(self, user=None, screen_name=None):
        statuses = []
        if user is not None:
            statuses = self.api.GetUserTimeline(user)
        elif screen_name is not None:
            statuses = self.api.GetUserTimeline(screen_name=screen_name)
        else:
            raise ValueError("Must provide either user or screen_name")
        return statuses

    def get_screen_name(self, user):
        u = self.api.GetUser(user)
        return u.screen_name

    def get_user(self, screen_name):
        u = self.api.GetUser(screen_name=screen_name)
        return u.id


def test_get_user():
    api = TwitterAPI()
    assert api.get_screen_name(25073877) == 'realDonaldTrump'
    assert api.get_user('realDonaldTrump') == 25073877