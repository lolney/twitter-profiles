from pycorenlp import StanfordCoreNLP
import json

CORENLP_DIRECTORY = r'/Users/Luke/Downloads/stanford-corenlp-full-2017-06-09'

class NLPWrapper:

    def __init__(self):
        self.nlp = StanfordCoreNLP('http://localhost:9000')

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
        punctuation = ['.','?','!']
        modtweets = map(lambda t : t if t[len(t) - 1] in punctuation else t + '.', tweets)
        print modtweets
        text = " ".join(modtweets).encode('ascii','replace')
        sentences = self.openie(text)
        filtered = filter(lambda s : s['relation'] in relations, sentences)
        return [s['object'] for s in filtered]

def test():
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
    nlp_wrapper2("I am a professional photographer who lives in Boise, ID")

if __name__ == "__main__":
    main()