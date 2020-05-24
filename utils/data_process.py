import re
from pymystem3 import Mystem
import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from tqdm import tqdm
import functools
import os

def single_call(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if not inner.called or not os.path.exists('processed.pickle') or not os.stat('processed.pickle').st_size:
            res = fn(*args, **kwargs)
            inner.called = True
            return res 
    inner.called = False
    return inner


@single_call
def process_text(text, min_word_size=4, min_sent_size=10, extra_stop=None, remove_short=True):
    html_cleaner = re.compile('<.*?>')
    cyrillic = re.compile(r'[^а-яА-Я ]')
    esc_punctuation = re.compile('[%s]' % re.escape(string.punctuation))
    extra_spaces = re.compile(r'\s{2,}')
    stop_list = stopwords.words('russian')
    if extra_stop:
        stop_list.extend([''])
    lmtzr = Mystem()
    
    n_sents = len(text)
    for i in tqdm(range(n_sents)):
        # html removal
        text[i] = html_cleaner.sub(' ', text[i]) # there's NO NoneType error
        # punctuation and numbers removal
        text[i] = esc_punctuation.sub(' ', text[i])
        # leaving only cyrillic words
        text[i] = cyrillic.sub(' ', text[i])
        # extrace spacing
        text[i] = extra_spaces.sub(' ', text[i])
        # lemmatization (Hint: look to pymystem3 docs)
        text[i] = ''.join(lmtzr.lemmatize(text[i])).strip()
        # stopwords removal + lowercasing
        text[i] = ' '.join([word.lower() for word in text[i].split() \
                            if len(word) >= min_word_size and word not in stop_list])
        
    text = [sent for sent in text if len(sent) >= min_sent_size]    
    print('done!')
    return text