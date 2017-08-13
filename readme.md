# Running a Stanford CoreNLP server

Download the CoreNLP library from https://stanfordnlp.github.io/CoreNLP/, then navigate to the CoreNLP directory and run:

``` java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 150000 ```

# Running the webserver

Install requirements
```pip install -r requirements.txt
sudo python -m textblob.download_corpora```

Running:
```cd twitter_profiles
FLASK_APP=twitter-profiles.py python -m flask run```