import pandas as pd
import plotly

import streamlit as st

@st.cache_data
def get_matrix_bert() -> plotly.graph_objects.Figure:
    with open("resources/conv_matrix_bert.json", "r") as fig:
        return plotly.io.from_json(fig.read())

@st.cache_data
def get_matrix_spacy_clean() -> plotly.graph_objects.Figure:
    with open("resources/conv_matrix_spacy_clean.json", "r") as fig:
        return plotly.io.from_json(fig.read())

conv_results = [
    ["CodeBERT", 0.86, 0.86, 0.79, 0.79],
    ["spaCy Clean", 0.81, 0.81, 0.76, 0.76],
    ["spaCy Dirty", 0.78, 0.79, 0.74, 0.74],
]

df_conv = pd.DataFrame(
    conv_results,
    columns=["Embedding", "Accuracy", "Avg. Precision", "Avg. Recall", "Avg. F1-Score"],
)

"""
# Convolutional
"""
st.dataframe(df_conv, hide_index=True)

"""
## CodeBERT
"""
st.plotly_chart(get_matrix_bert())

"""
## Spacy Clean 
"""
st.plotly_chart(get_matrix_spacy_clean())

