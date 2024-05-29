import plotly

import streamlit as st


@st.cache_data
def get_loc() -> plotly.graph_objects.Figure:
    with open("resources/lines_of_code_per_lang_augment.json", "r") as fig:
        return plotly.io.from_json(fig.read())


@st.cache_data
def get_entries() -> plotly.graph_objects.Figure:
    with open("resources/entries_per_lang_aungment.json", "r") as fig:
        return plotly.io.from_json(fig.read())

"""
# Data Augmentation

1. For each entry
2. Take its source code
3. Split them by lines of code, each chunk must have roughly 512 terms (tokens)
4. Add chunks to a new dataframe until an upper limit is met
"""

"""
We can use our defined function `gen_chunk_entries` with the dataframe from the `dataset.csv`. The dataframe must have a `source` field with all source code from the `file_path`:

```py
df = gen_chunk_entries(df)
```
"""

st.plotly_chart(get_entries())


"""
```py
def gen_chunk_entries(df, ENTRIES=3000, MAX_CHARS=512) -> pd.DataFrame:
    status = {}
    new_rows = []

    for lang in list(TARGET):
        status[lang] = 0

    with tqdm(total=ENTRIES * len(TARGET), position=0, leave=True) as pbar:
        for _, row in df.iterrows():
            lang = row.language

            if status[lang] < ENTRIES:
                for chunk in split_code_into_chunks(row.source, MAX_CHARS):
                    if status[lang] < ENTRIES:
                        new_rows.append({"language": lang, "source": chunk})
                        status[lang] += 1
                        pbar.update()

    tqdm._instances.clear()
    return pd.DataFrame(new_rows)
```

"""

st.plotly_chart(get_loc())
