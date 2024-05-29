import pandas as pd
import plotly

import streamlit as st


@st.cache_data
def get_matrix_bert() -> plotly.graph_objects.Figure:
    with open("resources/rforest_matrix_bert.json", "r") as fig:
        return plotly.io.from_json(fig.read())


@st.cache_data
def get_matrix_tfidf_clean() -> plotly.graph_objects.Figure:
    with open("resources/rforest_matrix_tfifd_clean.json", "r") as fig:
        return plotly.io.from_json(fig.read())


@st.cache_data
def get_matrix_spacy_clean() -> plotly.graph_objects.Figure:
    with open("resources/rforest_matrix_spacy_clean.json", "r") as fig:
        return plotly.io.from_json(fig.read())


rforest_results = [
    ["CodeBERT", 0.93, 0.94, 0.92, 0.92],
    ["TF-IDF Clean", 0.94, 0.95, 0.92, 0.93],
    ["TF-IDF Dirty", 0.91, 0.93, 0.87, 0.88],
    ["spaCy Clean", 0.81, 0.83, 0.76, 0.76],
    ["spaCy Dirty", 0.75, 0.77, 0.72, 0.72],
]

df_rforest = pd.DataFrame(
    rforest_results,
    columns=["Embedding", "Accuracy", "Avg. Precision", "Avg. Recall", "Avg. F1-Score"],
)

"""
# Random Forest

*Hyper-parameters:* 
- $(C = 12)$
"""
st.dataframe(df_rforest, hide_index=True)

"""
## CodeBERT
"""

st.plotly_chart(get_matrix_bert())

"""
## TF-IDF Clean
"""

st.plotly_chart(get_matrix_tfidf_clean())

"""
## Spacy Clean
"""

st.plotly_chart(get_matrix_spacy_clean())
