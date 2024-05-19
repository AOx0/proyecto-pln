# proyecto-pln

<div id="user-content-toc">
  <ul>
    <li><a href="#dependencies">Dependencies</a></li>
    <li><a href="#dataset">Dataset</a>
      <ul>
        <li><a href="#clean">Source code cleaning</a>
          <ul>
            <li><a href="#ahead-of-time">Ahead-of-time</a></li>
            <li><a href="#in-time">In-time</a></li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</div>

## Dependencies

This project uses [rye], [just] and the Nightly Rust compiler via [rustup].

## Dataset

The dataset the project uses is available at [kaggle]. The models are trained using a cleaned up version from the sources of the dataset where all comments are removed per programming language.

### Clean

There are two strategies to clean the source codes:
  - For one *ahead-of-time* cleanup you can use the `cleaner` cli (available at `./cleaner-cli`) to clean all sources once before the processing and training.
  - For an *in-time* cleaning on Python you can use the `cleaner` library (available at `./cleaner-py`), the library is also useful for cleaning arbitrary user input for its classification.

Both straegies use the rust-based implementation found at `./cleaner-lib`, the implementation first tries to match to a multiline comment block and fallbacks to single-line comments.

#### Ahead-of-time

The `cleaner` cli tool receives as input the file/dir where to look for matching blocks for deletion in-place with the given list of opening and closing sequences with `--open` and `--close` and the sequences that start a single-line comment block with `--single-line`.

For example, to clean all comments on all HTML files we can invoke the cli program the following way:
```sh
cleaner html_files/ --open "<!--" --close "'-->'"
```

Note the closing multiline block comment that starts with `--` (`-->`) is wrapped with single quotes `''` to be able to parse the argument correctly. All tokens that start with `--` must be wrapped the same way. 

Similarly, to clean all comments for a directory of ruby and lua source files we can use the command:
```sh
cleaner ruby_files/ --open "=begin" --close "=end" --single-line "#"
cleaner lua_files/ --open "'--[['" --close "'--]]'" --single-line "'--'"
```

There's a script to automatically clean all top langs (+100k lines of code) at `notebooks/clean.py`. Just make sure to change de hardcoded path to the directory of source files that was downloaded from [kaggle].
```sh
python scripts/clean_comments.py
```
#### In-time

Inside the `cleaner-py` there's a [maturin] project that creates bindings to the Rust `cleaner-py` library that are useful from Python. This provides the ability to clean source code as needed instead of doing it once for all the source files, and the ability to clean user input the same way the training data was cleaneas, and the ability to clean user input with the exactme way as the training dat cle



[rye]: https://github.com/astral-sh/rye
[just]: https://github.com/casey/just
[rustup]: https://www.rust-lang.org/tools/install
[kaggle]: https://www.kaggle.com/datasets/joonasyoon/file-format-detection
[maturin]: https://github.com/PyO3/maturin
