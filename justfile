install-cleaner:
    cd cleaner-py && VIRTUAL_ENV='{{justfile_directory()}}/.venv/' maturin develop --release

streamlit:
    . {{justfile_directory()}}/.venv/bin/activate && streamlit run streamlit/main.py
