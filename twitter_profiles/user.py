from textblob import TextBlob
from textblob.np_extractors import ConllExtractor

def profession():
    extractor = ConllExtractor()
    tweet = TextBlob("I am a professional photographer who lives in Boise, ID", np_extractor=extractor)
    return tweet.noun_phrases[0]

def main():
    print profession()

if __name__ == "__main__":
    main()

