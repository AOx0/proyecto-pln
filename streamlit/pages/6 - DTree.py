import pandas as pd
import plotly

import streamlit as st


@st.cache_data
def get_matrix_bert() -> plotly.graph_objects.Figure:
    with open("resources/dtree_matrix_bert.json", "r") as fig:
        return plotly.io.from_json(fig.read())


@st.cache_data
def get_matrix_tfidf_clean() -> plotly.graph_objects.Figure:
    with open("resources/dtree_matrix_tfidf_clean.json", "r") as fig:
        return plotly.io.from_json(fig.read())


@st.cache_data
def get_matrix_tfidf_dirty() -> plotly.graph_objects.Figure:
    with open("resources/dtree_matrix_tfidf_dirty.json", "r") as fig:
        return plotly.io.from_json(fig.read())


@st.cache_data
def get_matrix_spacy_clean() -> plotly.graph_objects.Figure:
    with open("resources/dtree_matrix_spacy_clean.json", "r") as fig:
        return plotly.io.from_json(fig.read())


@st.cache_data
def get_matrix_spacy_dirty() -> plotly.graph_objects.Figure:
    with open("resources/dtree_matrix_spacy_dirty.json", "r") as fig:
        return plotly.io.from_json(fig.read())


dtree_results = [
    ["CodeBERT", 0.78, 0.75, 0.75, 0.75],
    ["TF-IDF Clean", 0.89, 0.88, 0.88, 0.88],
    ["TF-IDF Dirty", 0.82, 0.81, 0.79, 0.80],
    ["spaCy Clean", 0.62, 0.58, 0.58, 0.58],
    ["spaCy Dirty", 0.52, 0.50, 0.50, 0.50],
]

df_dtree = pd.DataFrame(
    dtree_results,
    columns=["Embedding", "Accuracy", "Avg. Precision", "Avg. Recall", "Avg. F1-Score"],
)

"""
# Decision Tree
"""
st.dataframe(df_dtree, hide_index=True)


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
