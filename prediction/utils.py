import pickle
import torch
import transformers as tfm
import numpy as np
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

REPLACE_BY_SPACE_RE = re.compile(r'[/(){}\[\]\|@,;]') 
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

production = pickle.load(open(r"prediction/production.pth", 'rb'))

#requirements 
WORDS_TO_INDEX = production["WORDS_TO_INDEX"]
DICT_SIZE = production["DICT_SIZE"]
classifier_mybag = production["classifier_mybag"]
tfidf_vectorizer = production["tfidf_vectorizer"]
classifier_tfidf = production["classifier_tfidf"]
classifier_bert = production["classifier_bert"]
#max_input_length = production["max_input_length"]

# For DistilBERT:
# model_class, tokenizer_class, pretrained_weights = (tfm.DistilBertModel, tfm.DistilBertTokenizer, 'distilbert-base-uncased')

## For BERT :
model_class, tokenizer_class, pretrained_weights = (tfm.BertModel, tfm.BertTokenizer, 'bert-base-uncased')

# Load pretrained model/tokenizer
tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
#max_input_length = tokenizer.max_model_input_sizes['distilbert-base-uncased']
max_input_length = tokenizer.max_model_input_sizes['bert-base-uncased']

model = model_class.from_pretrained(pretrained_weights)
model = model.to(device)

def text_prepare(text):
    """
        text: a string
        return: modified initial string
    """
    text = text.lower() # lowercase text
    text = re.sub(REPLACE_BY_SPACE_RE, ' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = re.sub(BAD_SYMBOLS_RE, '', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join([word for word in text.split() if word not in STOPWORDS]) # delete stopwords from text
    return text

def my_bag_of_words(text, words_to_index, dict_size):
    """
        text: a string
        dict_size: size of the dictionary
        
        return a vector which is a bag-of-words representation of 'text'
    """
    result_vector = np.zeros(dict_size)
    for item in text.split():
        if item in words_to_index.keys():
            result_vector[words_to_index[item]] += 1
    return result_vector

def mybag_predict(eula):
    vec = my_bag_of_words(text_prepare(eula) , WORDS_TO_INDEX, DICT_SIZE)
    output = classifier_mybag.predict([vec])[0]
    return "EULA acceptable" if output == 1 else "EULA unacceptable"

def tfidf_predict(eula):
    vec = tfidf_vectorizer.transform([text_prepare(eula)])
    output = classifier_tfidf.predict(vec)[0]
    return "EULA acceptable" if output == 1 else "EULA unacceptable"

def bert_predict(eula):
  
  tokens = tokenizer.tokenize(eula)
  tokens = tokens[:max_input_length-2]
  init_token_idx = tokenizer.cls_token_id
  eos_token_idx = tokenizer.sep_token_id
  indexed = [init_token_idx] + tokenizer.convert_tokens_to_ids(tokens) + [eos_token_idx]
  tensor = torch.LongTensor(indexed).to(device)
  tensor = tensor.unsqueeze(0)
  with torch.no_grad():
        pooled_output, _ = model(tensor)
  vec = pooled_output[:,0,:].cpu().numpy()
  output = classifier_bert.predict(vec)[0]
  return "EULA acceptable" if output == 1 else "EULA unacceptable"
  
  # todo 
  #return tfidf_predict(eula)
  


def predict(model_name, eula):
  
  if model_name == "Bag of word":
    return mybag_predict(eula)
  elif model_name == "TD-IDF":
    return tfidf_predict(eula)
  elif model_name == "BERT":
    return bert_predict(eula)