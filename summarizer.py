import heapq
import string
from goose3 import Goose
import nltk
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

nltk.download('punkt')

factory = StopWordRemoverFactory()
stopwords = factory.get_stop_words()

def extract_article_text(url):
    g = Goose()
    article = g.extract(url)
    return article.cleaned_text, article.title

def preproccess(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords and word not in string.punctuation]
    return ' '.join(tokens)

def summarize_text(text, number_of_sentences=3, percentage=0):
    formatted_text = preproccess(text)
    words = nltk.word_tokenize(formatted_text)

    word_frequency = {}
    for word in words:
        word_frequency[word] = word_frequency.get(word, 0) + 1

    if not word_frequency:
        return [], []

    highest_frequency = max(word_frequency.values())
    for word in word_frequency:
        word_frequency[word] /= highest_frequency

    sentence_list = nltk.sent_tokenize(text)
    score_sentences = {}

    for sentence in sentence_list:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_frequency:
                score_sentences[sentence] = score_sentences.get(sentence, 0) + word_frequency[word]

    jumlah = max(1, int(len(sentence_list) * percentage)) if percentage > 0 else min(number_of_sentences, len(sentence_list))
    best_sentences = heapq.nlargest(jumlah, score_sentences, key=score_sentences.get)

    return sentence_list, best_sentences
