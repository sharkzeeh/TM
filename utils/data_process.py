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
        if not inner.called or not os.path.exists('processed.pickle') or not os.stat(path).st_size:
            fn(*args, **kwargs)
            inner.called = True
    inner.called = False
    return inner


@single_call
def process_text(text, min_word_size=2, min_sent_size=3, remove_short_sentenses=True):
    html_cleaner = re.compile('<.*>')
    cyrillic = re.compile(r'[^а-я ]')
    esc_punctuation = re.compile('[%s]' % re.escape(string.punctuation))
    extra_spaces = re.compile(r'\s+')

    stop = stopwords.words('russian')
    lmtzr = Mystem()
    
    n_sents = len(text)
    for i in tqdm(range(n_sents)):
        # html removal

        try:
            text[i] = html_cleaner.sub(' ', text[i]) # there's NO NoneType error
        except TypeError:
            # text[i] = ''
            print(f'deleting {text[i]} for some reason...')
            del text[i]
            continue

        # make all words lowercased
        # stopwords removal (Hint: look to nltk docs)
        text[i] = ' '.join([word.lower() for word in text[i].split() \
                            if not word in stop and len(word) > min_word_size])

        # punctuation and numbers removal
        text[i] = esc_punctuation.sub(' ', text[i])
        # leaving only cyrillic words
        text[i] = cyrillic.sub(' ', text[i])
        # extrace spacing
        text[i] = extra_spaces.sub(' ', text[i])
        # lemmatization (Hint: look to pymystem3 docs)
        text[i] = ''.join(lmtzr.lemmatize(text[i])).strip()

    if remove_short_sentenses:
        print('removing short words...')
        # remove texts with less than `min_sent_size` words after lemmatization   
        text = [text[i] for text[i] in text if len(text[i].split()) > min_sent_size]
    print('done!')

    return text