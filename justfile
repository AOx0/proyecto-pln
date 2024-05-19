install-cleaner:
    cd cleaner-py && VIRTUAL_ENV='{{justfile_directory()}}/.venv/' maturin develop --release

install-kernel:
    python -m ipykernel install --user --name=proyecto-pln

uninstall-kernel:
    jupyter kernelspec remove proyecto-pln

streamlit:
    . {{justfile_directory()}}/.venv/bin/activate && streamlit run streamlit/main.py
