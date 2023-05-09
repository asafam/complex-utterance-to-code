import nltk
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import SmoothingFunction
from nltk.corpus import stopwords
import string
import warnings

warnings.filterwarnings("ignore")
nltk.download("stopwords", quiet=True)

def tokenize(text, filter_stopwords=False):
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]
    if filter_stopwords:
        stop_tokens = set(stopwords.words("english") + list(string.punctuation))
        tokens = (
            [w.lower() for w in tokens if not w.lower() in stop_tokens]
            if all(w in stop_tokens for w in tokens)
            else tokens
        )
    return tokens


def compute_bleu_score(a, b, weights=(1.0, 0.0, 0.0, 0.0), filter_stopwords=False):
    hypothesis = tokenize(a, filter_stopwords=filter_stopwords)
    reference = tokenize(b, filter_stopwords=filter_stopwords)
    chencherry = SmoothingFunction()
    bleu_score = nltk.translate.bleu_score.sentence_bleu(
        [reference], hypothesis, weights, smoothing_function=chencherry.method1
    )
    return bleu_score
