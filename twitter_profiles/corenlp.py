from pycorenlp import StanfordCoreNLP
import json

CORENLP_DIRECTORY = r'/Users/Luke/Downloads/stanford-corenlp-full-2017-06-09'

class Compounds:

    def __init__(self, sentence):
        self.compounds_list = filter(lambda x: x['dep'] == 'compound', sentence['basicDependencies'])
        self.compounds_dict = {}

    def try_insert(self, token):
        for compound in self.compounds_list:
            if compound['governor'] == token['index'] or compound['dependent'] == token['index']:
                    try:
                        self.compounds_dict[compound['governor']].append(token)
                    except:
                        self.compounds_dict[compound['governor']] = [token]
                    return True
        return False

    def return_list(self):
        tokens_groupings = [sorted(x, lambda a,b: cmp(a['index'],b['index']))
            for x in self.compounds_dict.values()]
        words = [[token['word'] for token in tokens] for tokens in tokens_groupings]
        return map(lambda x: " ".join(x), words)


class NLPWrapper:

    def __init__(self):
        self.nlp = StanfordCoreNLP('http://localhost:9000')

    def clean_tweets(self, tweets):
        punctuation = ['.','?','!']
        modtweets = map(lambda t : t if t[len(t) - 1] in punctuation else t + '.', tweets)
        text = " ".join(modtweets).encode('ascii','replace')
        return text

    def parse(self, tweet):
        output = self.nlp.annotate(tweet, properties=
        {'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse','outputFormat':'json'})
        return [s['parse'] for s in output['sentences']]

    def openie(self, text):
        output = self.nlp.annotate(text, properties=
        {'annotators': 'tokenize,ssplit,pos,depparse,natlog,openie','outputFormat':'json'})
        outlist = []
        for s in output['sentences']:
            if len(s['openie']) > 0:
                outlist.append(s['openie'][0])
        return outlist

    def openie_relation(self, tweets, relations):
        text = self.clean_tweets(tweets)
        sentences = self.openie(text)
        filtered = filter(lambda s : s['relation'] in relations, sentences)
        return [s['object'] for s in filtered]

    def extract_nouns(self, output):
        nouns = []
        for sentence in output['sentences']:
            compounds = Compounds(sentence)
            for token in sentence['tokens']:
                if token['pos'] in ['NNP','VBG','NN']:
                    word = token['word']
                    inserted = compounds.try_insert(token)
                    if not inserted:
                        nouns.append(word)
            nouns += compounds.return_list()
        return nouns
                    

    def entities(self, tweets):
        text = self.clean_tweets(tweets)
        output = self.nlp.annotate(text, properties=
        {'annotators': 'tokenize,ssplit,pos,depparse','outputFormat':'json'});
        return self.extract_nouns(output)

def print_example():
    with open(CORENLP_DIRECTORY + "/presidents.txt.json") as fp:
        result = json.load(fp)
        for sentence in result["sentences"]:
            for token in sentence["tokens"]:
                if token['ner'] != 'O':
                    print token['ner']

class Parser:

    def Parser(string):
        self.string = string # need to make iterator

    def expr():
        token1 = next(self.string)
        token2 = next(self.string)
        if token2 == '(':
            token2 = None
            self.expr()
        while self.string.hasNext():
            n = next(self.string)
            if n == ')':
                return ParseTree(word=token2, pos=token1)
            elif n == '(':
                self.expr()
            else:
                outstring = outstring + n

class ParseTree:
    def ParseTree(word, pos):
        self.word = word
        self.pos = pos

def main():
    print "empty"

if __name__ == "__main__":
    main()

def test_nouns():
    nlp = NLPWrapper()
    tweets = ["My name is Ho Chi Mihn from New York", "I like barn raising and flying."]
    answers = sorted(['name', "New York","Ho Chi Mihn", "barn raising","flying"])
    assert sorted(nlp.entities(tweets)) == answers
