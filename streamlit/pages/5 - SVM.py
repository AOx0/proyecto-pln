import pandas as pd
import plotly

import streamlit as st


@st.cache_data
def get_matrix_bert() -> plotly.graph_objects.Figure:
    with open("resources/svm_matrix_bert.json", "r") as fig:
        return plotly.io.from_json(fig.read())

@st.cache_data
def get_matrix_tfidf_clean() -> plotly.graph_objects.Figure:
    with open("resources/svm_matrix_tfidf_clean.json", "r") as fig:
        return plotly.io.from_json(fig.read())

@st.cache_data
def get_matrix_tfidf_dirty() -> plotly.graph_objects.Figure:
    with open("resources/svm_matrix_tfidf_dirty.json", "r") as fig:
        return plotly.io.from_json(fig.read())

@st.cache_data
def get_matrix_spacy_clean() -> plotly.graph_objects.Figure:
    with open("resources/svm_matrix_spacy_clean.json", "r") as fig:
        return plotly.io.from_json(fig.read())

@st.cache_data
def get_matrix_spacy_dirty() -> plotly.graph_objects.Figure:
    with open("resources/svm_matrix_spacy_dirty.json", "r") as fig:
        return plotly.io.from_json(fig.read())


svm_results = [
    ["CodeBERT", 0.95, 0.95, 0.94, 0.95],
    ["TF-IDF Clean", 0.95, 0.96, 0.92, 0.93],
    ["TF-IDF Dirty", 0.93, 0.94, 0.90, 0.91],
    ["spaCy Clean", 0.88, 0.89, 0.86, 0.87],
    ["spaCy Dirty", 0.86, 0.87, 0.84, 0.85],
]

df_svm = pd.DataFrame(
    svm_results,
    columns=["Embedding", "Accuracy", "Avg. Precision", "Avg. Recall", "Avg. F1-Score"],
)

"""
# SVM

*Hyper-parameters:* 
- $(C = 12)$
"""
st.dataframe(df_svm, hide_index=True)

"""
## CodeBERT
"""

st.plotly_chart(get_matrix_bert())

"""
## TF-IDF Clean
"""

st.plotly_chart(get_matrix_tfidf_clean())

"""
## TF-IDF Dirty
"""

st.plotly_chart(get_matrix_tfidf_dirty())


"""
## Spacy Clean
"""

st.plotly_chart(get_matrix_spacy_clean())

"""
## Spacy Dirty
"""
st.plotly_chart(get_matrix_spacy_dirty())
