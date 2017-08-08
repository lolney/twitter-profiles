from textblob import TextBlob
from textblob.np_extractors import ConllExtractor
from textblob.taggers import NLTKTagger
from textblob.parsers import PatternParser
import tweets
import pattern
from pattern.text import find_relations
from corenlp import NLPWrapper

TWEET = "I am a professional photographer who lives in Boise, ID"
TWEET1 = "I work as a professional photographer"

def apply_tuple(fn, lst, sum1, sum2):
    if(len(lst) == 0):
        return []
    else:
        elem = lst.pop()
        result = fn(elem, sum1, sum2)
        nlst = apply_tuple(fn, lst, result[1], result[2])
        nlst.append(result[0])   
        return nlst

def _parse_pattern(word, i, j):
    parts = word.split("/")
    chunk = parts[2].split("-")
    pnp = parts[3].split("-")
    relation = parts[4].split("-")

    if(len(chunk) == 1):
        chunk = [None,None]
    if(len(pnp) == 1):
        pnp = [None,None]
    if(len(relation) == 1 or len(relation) == 2):
        relation = [None, None, None]

    return ({
        "word": parts[0],
        "tag": parts[1],
        "chunk": chunk[1],
        "chunk_index": i + 1 if chunk[0] == 'i' else 0,
        "pnp":  pnp[1],
        "pnp_index": j + 1 if pnp[0] == 'i' else 0,
        "relation": relation[1],
        "relation_anchor": relation[2]
    }, i+1, j+1)

def parse_pattern(lst):
    return apply_tuple(_parse_pattern, lst.split(" "), 0, 0)

class User:

    def __init__(self, user=None, screen_name=None):
        if user is None and screen_name is None:
            raise ValueError("Must initialize with either user id or screen name")
        self.screen_name = screen_name
        self.user = user
        self.nlp = NLPWrapper()

    def profession(self):
        extractor = ConllExtractor()
        tweet = TextBlob(TWEET, np_extractor=extractor)
        return tweet.noun_phrases[0]

    def interests(self):
        statuses = self.get_statuses()
        candidates = self.nlp.openie_relation(statuses, ['like','love'])
        return candidates

    def location(self):
        statuses = self.get_statuses()
        candidates = self.nlp.openie_relation(statuses, ['live in'])
        return candidates

    def get_statuses(self):
        if self.screen_name is not None:
            return [status.text for status in tweets.get_statuses(screen_name=self.screen_name)]
        elif self.user is not None:
            return [status.text for status in tweets.get_statuses(self.user)]

def trump_test():
    extractor = ConllExtractor()
    nltk_tagger = NLTKTagger()
    statuses = tweets.get_statuses(user=25073877)

    for status in statuses:
        tweet = TextBlob(status.text, np_extractor=extractor, pos_tagger=nltk_tagger)
        if "I" in tweet.words: 
            print status.text
            for pos_tag in tweet.pos_tags:
                if pos_tag[1] in ["VB","VBD","VBG","VBN","VBP","VBZ"]:
                    print pos_tag[0]
            for noun in tweet.noun_phrases:
                print noun

def main():
    interests('billclinton')

if __name__ == "__main__":
    main()

