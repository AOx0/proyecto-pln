import pandas as pd
import plotly

import streamlit as st

@st.cache_data
def get_matrix_bert() -> plotly.graph_objects.Figure:
    with open("resources/fnn_matrix_bert.json", "r") as fig:
        return plotly.io.from_json(fig.read())

@st.cache_data
def get_matrix_spacy_clean() -> plotly.graph_objects.Figure:
    with open("resources/fnn_matrix_spacy_clean.json", "r") as fig:
        return plotly.io.from_json(fig.read())

fnn_results = [
    ["CodeBERT", 0.94, 0.94, 0.93, 0.94],
    ["spaCy Clean", 0.86, 0.80, 0.80, 0.80],
    ["spaCy Dirty", 0.84, 0.85, 0.80, 0.80],
]

df_fnn = pd.DataFrame(
    fnn_results,
    columns=["Embedding", "Accuracy", "Avg. Precision", "Avg. Recall", "Avg. F1-Score"],
)

"""
# FNN
"""
st.dataframe(df_fnn, hide_index=True)

"""
## CodeBERT
"""
st.plotly_chart(get_matrix_bert())

"""
## Spacy Clean 
"""
st.plotly_chart(get_matrix_spacy_clean())

