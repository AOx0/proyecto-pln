import re
from pickle import load

import cleaner
import contractions
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
import spacy
import tensorflow as tf
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
def get_dtree_spacy() -> SVC:
    with open("modelos/dtree_spacy.pkl", "rb") as f:
        return load(f)


@st.cache_data
def get_dtree_tfidf() -> SVC:
    with open("modelos/dtree_tfidf.pkl", "rb") as f:
        return load(f)


@st.cache_data
def get_rforest_bert() -> SVC:
    with open("modelos/rforest_bert.pkl", "rb") as f:
        return load(f)


@st.cache_data
def get_rforest_spacy() -> SVC:
    with open("modelos/rforest_spacy.pkl", "rb") as f:
        return load(f)


@st.cache_data
def get_rforest_tfidf() -> SVC:
    with open("modelos/rforest_tfidf.pkl", "rb") as f:
        return load(f)


@st.cache_data
def get_tfidf_vectorizer() -> SVC:
    with open("modelos/tfidf_vectorizer.pkl", "rb") as f:
        return load(f)


@st.cache_data
def get_fnn_bert() -> SVC:
    return tf.keras.models.load_model("notebooks/fnn_bert.keras")


@st.cache_data
def get_fnn_spacy() -> SVC:
    return tf.keras.models.load_model("notebooks/fnn_spacy.keras")


@st.cache_data
def get_conv_bert() -> SVC:
    return tf.keras.models.load_model("notebooks/conv_bert.keras")


@st.cache_data
def get_conv_spacy() -> SVC:
    return tf.keras.models.load_model("notebooks/conv_spacy.keras")


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


def predict_tfidf(source, predict, result, multi=[], single=[]):
    global tfidf_vectorizer
    # cleaned = clean(ccleaner.clean_string(source, multi, single), "")
    vec = tfidf_vectorizer.transform([clean_extras(source)])
    resultado = predict(vec)

    return result(resultado)


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
svm_tfidf_model = get_svm_tfidf()

dtree_bert_model = get_dtree_bert()
dtree_spacy_model = get_dtree_spacy()
dtree_tfidf_model = get_dtree_tfidf()

rforest_bert_model = get_rforest_bert()
rforest_spacy_model = get_rforest_spacy()
rforest_tfidf_model = get_rforest_tfidf()

bert_tokenizer = get_bert_tokenizer()
bert_model = get_bert_model()
tfidf_vectorizer = get_tfidf_vectorizer()

fnn_bert = get_fnn_bert()
fnn_spacy = get_fnn_spacy()

conv_bert = get_conv_bert()
conv_spacy = get_conv_spacy()

with st.sidebar:
    file = st.file_uploader("Upload source code")

if file is not None:
    contents = file.read().decode("utf-8")

    f"""
    # FNN
    ### **CodeBERT**: {predict_bert(contents,
        lambda vec: fnn_bert.predict(vec, verbose = 0),
        lambda res: TARGET[np.argmax(res)]
    )} 
    """

    valores = st.columns([1, 1, 1, 1])
    etiquetas = st.columns([1, 1, 1, 1])

    resultados = [
        (TARGET[i], resultado)
        for i, resultado in enumerate(
            predict_bert(
                contents,
                lambda vec: fnn_bert.predict(vec, verbose=0),
                lambda res: res[0],
            )
        )
    ]
    resultados.sort(key=lambda x: x[1], reverse=True)

    for i, resultado in enumerate(resultados[:4]):
        valores[i].title(f"{resultado[1] * 100.0:.2f} %")
    for i, resultado in enumerate(resultados[:4]):
        etiquetas[i].write(f"{resultado[0]}")

    f"""
    ### **spaCy**: {predict_spacy(contents,
        lambda vec: fnn_spacy.predict(vec, verbose = 0),
        lambda res: TARGET[np.argmax(res)]
    )} 
    """

    valores2 = st.columns([1, 1, 1, 1])
    etiquetas2 = st.columns([1, 1, 1, 1])

    resultados = [
        (TARGET[i], resultado)
        for i, resultado in enumerate(
            predict_spacy(
                contents,
                lambda vec: fnn_spacy.predict(vec, verbose=0),
                lambda res: res[0],
            )
        )
    ]
    resultados.sort(key=lambda x: x[1], reverse=True)

    for i, resultado in enumerate(resultados[:4]):
        valores2[i].title(f"{resultado[1] * 100.0:.2f} %")
    for i, resultado in enumerate(resultados[:4]):
        etiquetas2[i].write(f"{resultado[0]}")

    f"""
    # conv
    ### **CodeBERT**: {predict_bert(contents,
        lambda vec: conv_bert.predict(vec, verbose = 0),
        lambda res: TARGET[np.argmax(res)]
    )} 
    """

    valores = st.columns([1, 1, 1, 1])
    etiquetas = st.columns([1, 1, 1, 1])

    resultados = [
        (TARGET[i], resultado)
        for i, resultado in enumerate(
            predict_bert(
                contents,
                lambda vec: conv_bert.predict(vec, verbose=0),
                lambda res: res[0],
            )
        )
    ]
    resultados.sort(key=lambda x: x[1], reverse=True)

    for i, resultado in enumerate(resultados[:4]):
        valores[i].title(f"{resultado[1] * 100.0:.2f} %")
    for i, resultado in enumerate(resultados[:4]):
        etiquetas[i].write(f"{resultado[0]}")

    f"""
    ### **spaCy**: {predict_spacy(contents,
        lambda vec: conv_spacy.predict(vec, verbose = 0),
        lambda res: TARGET[np.argmax(res)]
    )} 
    """

    valores2 = st.columns([1, 1, 1, 1])
    etiquetas2 = st.columns([1, 1, 1, 1])

    resultados = [
        (TARGET[i], resultado)
        for i, resultado in enumerate(
            predict_spacy(
                contents,
                lambda vec: conv_spacy.predict(vec, verbose=0),
                lambda res: res[0],
            )
        )
    ]
    resultados.sort(key=lambda x: x[1], reverse=True)

    for i, resultado in enumerate(resultados[:4]):
        valores2[i].title(f"{resultado[1] * 100.0:.2f} %")
    for i, resultado in enumerate(resultados[:4]):
        etiquetas2[i].write(f"{resultado[0]}")
    f"""
    # SVM
    ### **CodeBERT**: {predict_bert(contents, 
        lambda vec: svm_bert_model.predict(vec),
        lambda res: TARGET[res[0]]
    )}
    ### **TF-IDF**: {predict_tfidf(contents,
        lambda vec: svm_tfidf_model.predict(vec),
        lambda res: TARGET[res[0]]
    )}
    ### **spaCy**: {predict_spacy(contents,
        lambda vec: svm_spacy_model.predict(vec),
        lambda res: TARGET[res[0]]
    )}
    """

    f"""
    # Random Forest
    ### **CodeBERT**: {predict_bert(contents,
        lambda vec: rforest_bert_model.predict(vec),
        lambda res: TARGET[res[0]]
    )}
    ### **TF-IDF**: {predict_tfidf(contents,
        lambda vec: rforest_tfidf_model.predict(vec),
        lambda res: TARGET[res[0]]
    )}
    ### **spaCy**: {predict_spacy(contents,
        lambda vec: rforest_spacy_model.predict(vec),
        lambda res: TARGET[res[0]]
    )}
    """

    f"""
    # Decision Tree
    ### **CodeBERT**: {predict_bert(contents,
        lambda vec: dtree_bert_model.predict(vec),
        lambda res: TARGET[res[0]]
    )}
    ### **TF-IDF**: {predict_tfidf(contents,
        lambda vec: dtree_tfidf_model.predict(vec),
        lambda res: TARGET[res[0]]
    )}
    ### **spaCy**: {predict_spacy(contents,
        lambda vec: dtree_spacy_model.predict(vec),
        lambda res: TARGET[res[0]]
    )}
    """
