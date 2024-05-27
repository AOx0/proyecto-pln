import re
from pickle import load

import cleaner
import contractions
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
import spacy
import torch
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC
from tqdm.notebook import tqdm
from transformers import AutoModel, AutoTokenizer

import streamlit as st

# nltk.download("stopwords")
# nltk.download("punkt")
# nltk.download("wordnet")

stopwords_en = stopwords.words("english")

lemmatizer = WordNetLemmatizer()


@st.cache_data
def get_bert_model():
    return AutoModel.from_pretrained("microsoft/codebert-base")


@st.cache_data
def get_bert_tokenizer():
    return AutoTokenizer.from_pretrained("microsoft/codebert-base")


nlp = spacy.load("en_core_web_lg")

tqdm.pandas()

TARGET = [
    "C",
    "C#",
    "C++",
    "Dart",
    "Elixir",
    "Go",
    "JSON",
    "Java",
    "Javascript",
    "Julia",
    "Kotlin",
    "Markdown",
    "Ruby",
    "Rust",
    "Python",
]


@st.cache_data
def get_svm_bert() -> SVC:
    with open("modelos/svm_bert.pkl", "rb") as f:
        return load(f)


@st.cache_data
def get_svm_tfidf() -> SVC:
    with open("modelos/svm_tfidf.pkl", "rb") as f:
        return load(f)


@st.cache_data
def get_svm_spacy() -> SVC:
    with open("modelos/svm_spacy.pkl", "rb") as f:
        return load(f)


@st.cache_data
def get_dtree_bert() -> SVC:
    with open("modelos/dtree_bert.pkl", "rb") as f:
        return load(f)


@st.cache_data
def get_tfidf_vectorizer() -> SVC:
    with open("modelos/tfidf_vectorizer.pkl", "rb") as f:
        return load(f)


def tokenize_bert(source: str):
    global bert_tokenizer
    tokens = bert_tokenizer.tokenize(
        source, return_tensors="pt", truncation=True, max_length=512
    )
    lemmas = [
        lemmatizer.lemmatize(token) for token in tokens if token not in stopwords_en
    ]
    return bert_tokenizer.convert_tokens_to_ids(lemmas)


def vectorize_bert(tokens) -> np.ndarray:
    global bert_model
    with torch.no_grad():
        outputs = bert_model(torch.tensor(tokens)[None, :])

    # We use the [CLS] token's embedding as the representation of the entire code snippet
    cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()

    return cls_embedding


def clean_comments(contents, language) -> str:
    delimiters = cleaner.lang(language)

    if delimiters is not None:
        contents = cleaner.string(contents, *delimiters)

    return contents


def clean_extras(contents) -> str:
    contents = re.sub(r"[\r]", "", contents)
    contents = re.sub(r"'[^']*'", "''", contents)
    contents = re.sub('"[^"]*"', '""', contents)
    contents = re.sub(r"\w{15,}", "", contents)
    contents = re.sub("[\n]{2,}", "\n", contents)
    contents = re.sub("[\t]{2,}", "\t", contents)
    contents = re.sub(r"[ ]+", " ", contents)

    contents = "\n".join(
        [line for line in contents.splitlines() if len(line.strip()) != 0]
    )

    return contents


def predict_bert(source, predict, result, multi=[], single=[]):
    # cleaned = clean(ccleaner.clean_string(source, multi, single), "")
    vec = vectorize_bert(tokenize_bert(clean_extras(source))).reshape(1, -1)
    resultado = predict(vec)

    return result(resultado)


def predict_svm_tfidf(source, verbose=False, multi=[], single=[]):
    global tfidf_vectorizer, svm_tfidf
    # cleaned = clean(ccleaner.clean_string(source, multi, single), "")
    vec = tfidf_vectorizer.transform([clean_extras(source)])
    resultado = svm_tfidf.predict(vec)

    return TARGET[resultado[0]]


def predict_spacy(source, predict, result, multi=[], single=[]):
    global svm_spacy_model
    # cleaned = clean(ccleaner.clean_string(source, multi, single), "")
    tokens = word_tokenize(clean_extras(source))

    # Porque queremos encontrar las palabras en el diccionario no usamos stemming
    lemmas = (
        lemmatizer.lemmatize(token) for token in tokens if token not in stopwords_en
    )

    resultado = " ".join(lemmas)
    vec = nlp(resultado).vector.reshape(1, -1)
    resultado = predict(vec)

    # return TARGET[resultado[0]]
    return result(resultado)


svm_bert_model = get_svm_bert()
svm_spacy_model = get_svm_spacy()
svm_tfidf = get_svm_tfidf()

dtree_bert_model = get_dtree_bert()

bert_tokenizer = get_bert_tokenizer()
bert_model = get_bert_model()
tfidf_vectorizer = get_tfidf_vectorizer()

with st.sidebar:
    file = st.file_uploader("Upload source code")

if file is not None:
    contents = file.read().decode("utf-8")

    f"""
    # SVM
    - CodeBERT: {predict_bert(contents, 
        lambda vec: svm_bert_model.predict(vec),
        lambda res: TARGET[res[0]]
    )}
    - TF-IDF: {predict_svm_tfidf(contents)}
    - spaCy: {predict_spacy(contents,
        lambda vec: svm_spacy_model.predict(vec),
        lambda res: TARGET[res[0]]
    )}
    """

    f"""
    # DTree
    - CodeBERT: {predict_bert(contents,
        lambda vec: dtree_bert_model.predict(vec),
        lambda res: TARGET[res[0]]
    )}
    - spaCy: {predict_spacy(contents,
        lambda vec: svm_spacy_model.predict(vec),
        lambda res: TARGET[res[0]]
    )}
    """
