#!/usr/bin/env python
# encoding: utf-8
"""
@author: Xin Jin
@contact: xinjin5991@gmail.com
"""

import json
import langid
import re
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import WordPunctTokenizer
from nltk.stem import SnowballStemmer

punctuations = [',', '.', '"', ':', ')', '(', '-', '!', '?', '|', ';', "'", '$', '&', '/', '[', ']', '>', '%', '=', '#',
                '*', '+', '\\', '•', '~', '@', '£',
                '·', '_', '{', '}', '©', '^', '®', '`', '<', '→', '°', '€', '™', '›', '♥', '←', '×', '§', '″', '′', 'Â',
                '█', '½', 'à', '…',
                '“', '★', '”', '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾', '═', '¦', '║', '―',
                '¥', '▓', '—', '‹', '─',
                '▒', '：', '¼', '⊕', '▼', '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲', 'è', '¸',
                '¾', 'Ã', '⋅', '‘', '∞',
                '∙', '）', '↓', '、', '│', '（', '»', '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'ï', 'Ø',
                '¹', '≤', '‡', '√', ]

abbreviation = {"no": "number", "no.": "number", "otp": "one time password", "dob": "date of birth",
                "d.o.b": "date of birth", "d.o.b.": "date of birth", "cvv": "card verification value",
                "ssn": "social security number", "if applicable": "optional", "if any": "optional",
                "lan": "local area network",
                "captcha": "completely automated public turing test to tell computers and humans apart",
                "atm": "automated teller machine", "sms": "short message service",
                "sim": "subscriber identification module",
                "url": "website", "uri": "website", 'e-mail': "email", "apt.": "apartment", "firstname": "first name",
                "lastname": "last name"}


class TextProcessor(object):

    def __init__(self, text):
        """
        :param text: string of text to be processed
        """
        self.text = str(text).lower()

    def remove_html_tags(self):
        """
        remove html tags from text, like "http://google.com <b here /b>" -> "http://google.com "
        :return: string of processed text
        """
        formatter = re.compile('<.*?>')
        return re.sub(formatter, '', self.text)

    def remove_punctuations(self):
        """
        remove punctuations from text, "hi, there" -> "hi there"
        :return: string of processed text
        """
        for punctuation in punctuations:
            if punctuation in self.text:
                self.text = self.text.replace(punctuation, '')
        return self.text

    def remove_numbers(self):
        """
        remove numbers from text
        :return: string of processed text
        """
        tokens = ToktokTokenizer().tokenize(self.text)
        tokens = [token.strip() for token in tokens]
        tokens = [token for token in tokens if not token.isnumeric()]
        return ' '.join(tokens)

    def replace_abbreviations(self):
        """
        replace abbreviations with corresponding text expressions
        :return: string of processed text
        """
        for key, value in abbreviation.items():
            if key == self.text or ' ' + key in self.text or key + ' ' in self.text:
                self.text = self.text + " " + value
        if "@" in self.text:
            self.text = self.text + " email"
        if "yyyy" in self.text and "mm" in self.text and "dd" in self.text:
            self.text = self.text + " date"
        if "yyyy" in self.text and "mm" not in self.text and "dd" not in self.text:
            self.text = self.text + " year"
        if "xxxx" in self.text:
            self.text = self.text + " phone number"
        if "#" in self.text:
            self.text = self.text + " number"
        return self.text

    def remove_stop_words(self, retain_list=None):
        """
        remove stop words from text
        :param retain_list: list of specific stop words that needs to be retained
        :return: string of processed text
        """
        if retain_list is None:
            retain_list = ['in', 'on', 'up']
        stop_words_list = nltk.corpus.stopwords.words('english')
        tokenizer = ToktokTokenizer()
        tokens = tokenizer.tokenize(self.text)
        tokens = [token.strip() for token in tokens]
        filtered_tokens = []
        for token in tokens:
            if token not in stop_words_list or token in retain_list:
                filtered_tokens.append(token)
        filtered_text = ' '.join(filtered_tokens)
        return filtered_text

    def lemma_text(self):
        """
        stem the words in other version to original ones in text, do not use stemming because stemming will change
        the word to format that glove cannot work on.
        :return: string of processed text
        """
        lemmatizer = WordNetLemmatizer()
        tokenizer = ToktokTokenizer()
        tokens = tokenizer.tokenize(self.text)
        tokens = [token.strip() for token in tokens]
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        return ' '.join(tokens)

    def stem_text(self):
        words = WordPunctTokenizer().tokenize(self.text)
        words = [SnowballStemmer('english').stem(w) for w in words]
        return " ".join(words)

    def filter_by_embedding(self, model):
        tokenizer = ToktokTokenizer()
        tokens = tokenizer.tokenize(self.text)
        tokens = [token.strip() for token in tokens]
        text_filtered = []
        for token in tokens:
            if token != '':
                try:
                    tmp = model[token]
                    text_filtered.append(token)
                except KeyError:
                    continue
        return ' '.join(text_filtered)

    def remove_url(self):
        return re.sub(r'^https?:\/\/.*[\r\n]*', '', self.text)

    def process(self, remove_stop_word=True):
        """
        process text in pipe line
        :param model_embedding: word embedding model
        :param use_model_filter: if True, it will remove words not in word embedding model
        :param remove_stop_word: if True, remove stop words from text
        :param stem_text: if True, stem the text
        :return: string of processed text
        """
        self.text = self.text.lower()
        self.text = self.replace_abbreviations()
        self.text = self.remove_html_tags()
        self.text = self.remove_punctuations()
        self.text = self.stem_text()
        if remove_stop_word:
            self.text = self.remove_stop_words()
        self.text = self.remove_numbers()
        return self.text

tp = TextProcessor("")

def preprocess_one_description(description, enable_langid=False):
    """
    preprocess one google play app description to generate input for classification
    :param description: string of description
    :param enable_langid: if True, use langid to filter the description as we only focus on English description
    :return: preprocessed text
    """
    tp.text = description
    language = langid.classify(tp.text)[0]
    if not enable_langid or language == "en":
        res = tp.process(remove_stop_word=True)
        return res
    else:
        print('[-]', "The language of this description is not English, discard it.")
        return res
