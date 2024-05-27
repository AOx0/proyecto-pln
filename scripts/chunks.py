import re

import cleaner
import nltk
import numpy as np
import pandas as pd
import torch
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")

stopwords_en = stopwords.words("english")

lemmatizer = WordNetLemmatizer()

bert_tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
bert_model = AutoModel.from_pretrained("microsoft/codebert-base")

tqdm.pandas()


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


def tokenize(source: str):
    tokens = bert_tokenizer.tokenize(
        source, return_tensors="pt", truncation=True, max_length=512
    )
    lemmas = [
        lemmatizer.lemmatize(token) for token in tokens if token not in stopwords_en
    ]
    return bert_tokenizer.convert_tokens_to_ids(lemmas)


def vectorize(tokens) -> np.ndarray:
    with torch.no_grad():
        outputs = bert_model(torch.tensor(tokens)[None, :])

    # We use the [CLS] token's embedding as the representation of the entire code snippet
    cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()

    return cls_embedding


def read_content(path, origin):
    path = origin + "/" + path

    file = open(path, "rb")
    contents = file.read().decode(errors="ignore")
    file.close()

    return contents


def split_code_into_chunks(code, max_chars):
    lines = code.split("\n")
    chunks = []
    current_chunk = []
    current_length = 0

    for line in lines:
        token_len = len(tokenize(line))
        if current_length + token_len + 1 > max_chars:
            chunks.append("\n".join(current_chunk))
            current_chunk = [line]
            current_length = token_len + 1  # +1 for the newline character
        else:
            current_chunk.append(line)
            current_length += token_len + 1  # +1 for the newline character

    # Add the last chunk
    # if current_chunk:
    # chunks.append('\n'.join(current_chunk))

    return chunks


def split_dataframe(df, n):
    """
    Splits a DataFrame into N roughly equal sub-dataframes.

    Parameters:
    df (pd.DataFrame): The DataFrame to split.
    n (int): The number of sub-dataframes to create.

    Returns:
    list of pd.DataFrame: A list containing the sub-dataframes.
    """
    # Calculate the number of rows per sub-dataframe
    k, m = divmod(len(df), n)

    # Create a list to hold the sub-dataframes
    sub_dfs = []

    # Iterate over the range of the number of sub-dataframes
    with tqdm(total=n, position=0, leave=True) as pbar:
        for i in range(n):
            # Calculate the start and end indices for each sub-dataframe
            start_idx = i * k + min(i, m)
            end_idx = (i + 1) * k + min(i + 1, m)

            # Append the sub-dataframe to the list
            sub_dfs.append(df.iloc[start_idx:end_idx])
            pbar.update()

    tqdm._instances.clear()
    return sub_dfs


def gen_chunk_entries(df: pd.DataFrame, ENTRIES=3000, MAX_CHARS=512) -> pd.DataFrame:
    status = {}
    bufs = {}

    for lang in list(TARGET):
        status[lang] = 0

    new_rows = []
    total = 0

    with tqdm(total=ENTRIES * len(TARGET), position=0, leave=True) as pbar:
        for _, row in df.iterrows():
            lang = row.language

            if status[lang] < ENTRIES:
                for chunk in split_code_into_chunks(row.source, MAX_CHARS):
                    if status[lang] < ENTRIES:
                        new_rows.append({"language": lang, "source": chunk})
                        status[lang] += 1
                        total += 1
                        pbar.update()

    tqdm._instances.clear()
    return pd.DataFrame(new_rows)


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

df = pd.read_csv("/home/ae/repos/archivos/dataset.csv")
df = df[df["language"].isin(TARGET)]

del df["file_size"]
del df["line_count"]
del df["extension"]

print("Reading contents...")
df["source"] = df["file_path"].progress_apply(
    lambda x: read_content(x, "/home/ae/repos/archivos/dataset")
)

mapper = {}
for i in range(len(TARGET)):
    mapper[TARGET[i]] = i

print("Generating labels...")
df["lang"] = df["language"].map(mapper)

df_clean = df.copy()
df_dirty = df.copy()

print("Cleaning contents on df_clean...")
df_clean["source"] = df_clean.progress_apply(lambda r: clean_comments(r.source, r.language), axis=1)


print("Cleaning extras on df_clean...")
df_clean["source"] = df_clean["source"].progress_apply(clean_extras)
print("Cleaning extras on df_dirty...")
df_dirty["source"] = df_dirty["source"].progress_apply(clean_extras)

chunks = 3000
print(f"Splitting in {chunks} chunks for each language for df_clean...")
df_clean_chunk: pd.DataFrame = gen_chunk_entries(df_clean, 3000)
print(f"Splitting in {chunks} chunks for each language for df_dirty...")
df_dirty_chunk: pd.DataFrame = gen_chunk_entries(df_dirty, 3000)

print("Saving chunks for df_clean_chunk ...")
df_clean_chunk.to_pickle("clean_chunks_no_str")
print("Saving chunks for df_dirty_chunk ...")
df_dirty_chunk.to_pickle("dirty_chunks_no_str")
