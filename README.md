Use the application by directly following this link : https://eulapp.herokuapp.com/

# Dependencies
* django
* sklearn
* numpy
* nltk
* numpy
* ktrain
* pandas
* ...

# User's Guide
## Setting up dependencies
```
pip install -r requirements.txt
```

All the pre-trained models, dictionaries and useful methods have been serialized and deposited in [production.pth](prediction/production.pth)

It is a dictionary containing the following elements:
- **WORDS_TO_INDEX** : Dictionary of words and their order in the vocabulary (Bag of words)
- **DICT_SIZE** : size of the dictionary (Bag of word)
- **classifier_mybag** : model of logistic regression based on the Bag of word
- **tfidf_vectorizer** : method to transform sentences into vectors (TF-IDF)
- **classifier_tfidf**: logistic regression model based on TF-IDF
- **classifier_bert** : logistic regression model based on BERT
- **max_input_length** : maximum length of sentences accepted by BERT

More details can be found in [utils.py](prediction/utils.py).

The first launch of the application takes a little time because bert pre-trained is loaded as well as his tokenizer: see [utils.py](prediction/utils.py).

You can also adapt the previous parameters by following the steps in this [notebook](https://colab.research.google.com/drive/1Ptq1A27ENcqqtcq2WmB6aztBc-qzBq_7#scrollTo=3QFCqOZ9hCb1).

## Launch the application
```
python manage.py runsever
```
http://localhost:8000/
