import pandas as pd
import plotly

import streamlit as st


@st.cache_data
def get_loc() -> plotly.graph_objects.Figure:
    with open("resources/lines_of_code_per_lang.json", "r") as fig:
        return plotly.io.from_json(fig.read())

@st.cache_data
def get_entries() -> plotly.graph_objects.Figure:
    with open("resources/entries_per_lang.json", "r") as fig:
        return plotly.io.from_json(fig.read())


fields = [
    [
        "id",
        "int",
        "A unique identifier per entry.",
    ],
    [
        "file_path",
        "str",
        "The path to a source code file.",
    ],
    [
        "file_size",
        "int",
        "The source file size in bytes.",
    ],
    [
        "line_count",
        "int",
        "Lines of code the file contains.",
    ],
    [
        "extension",
        "str",
        "The file extension the path has.",
    ],
    [
        "language",
        "str",
        "The name of the programming language.",
    ],
]
df_fields = pd.DataFrame(fields, columns=["Field", "Type", "Description"])


"""
# Data understanding

- 86,227 Source Code Files
- 77 Programming Languages
"""

"""
## Fields
"""

st.dataframe(df_fields, hide_index=True)

"""
## Unbalance:
- Languages like Rust have a lot of entries
- From within entries, lines of code are not balanced
"""

st.plotly_chart(get_entries())

st.plotly_chart(get_loc())

