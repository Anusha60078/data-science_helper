# ds_helper/text_cleaner.py

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download resources (only first time)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

class TextCleaner:
    def _init_(self, remove_stopwords=True, lemmatize=True):
        self.remove_stopwords = remove_stopwords
        self.lemmatize = lemmatize
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.filler_words = {"uh", "um", "like"}

    def clean(self, text):
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = nltk.word_tokenize(text)
        words = [w for w in words if w not in self.filler_words]
        if self.remove_stopwords:
            words = [w for w in words if w not in self.stop_words]
        if self.lemmatize:
            words = [self.lemmatizer.lemmatize(w) for w in words]

        return words