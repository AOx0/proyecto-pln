install-cleaner:
    cd cleaner-py && maturin build --release
    find '{{justfile_directory()}}/target/' -name '*.whl' | xargs -I {} rye add cleaner --absolute --path '{}'

uninstall-cleaner:
    rye remove cleaner

install-kernel:
    env PATH="{{justfile_directory()}}/.venv/lib/python3.12/site-packages:$PATH" ./.venv/bin/python -m ipykernel install --user --name=proyecto-pln

uninstall-kernel:
    jupyter kernelspec remove proyecto-pln

streamlit:
    . {{justfile_directory()}}/.venv/bin/activate && streamlit run streamlit/main.py
