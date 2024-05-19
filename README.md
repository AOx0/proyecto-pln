# proyecto-pln

## Dependencies

This project uses [rye], [just] and the Nightly Rust compiler via [rustup].

## Dataset

The dataset the project uses is available at [kaggle]. The models are trained using a cleaned up version from the sources of the dataset where all comments are removed per programming language.

There are two strategies to clean the source codes:
  - For one *ahead-of-time* cleanup you can use the `cleaner` cli (available at `./cleaner-cli`) to clean all sources once before the processing and training.
  - For an *in-time* cleaning on Python you can use the `ccleaner` library (available at `./cleaner-py`), the library is also useful for cleaning arbitrary user input for its classification.

Both straegies use the rust-based implementation found at `./cleaner-lib`, the implementation first tries to match to a multiline comment block and fallbacks to single-line comments.

### Ahead-of-time

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

### In-time



[rye]: https://github.com/astral-sh/rye
[just]: https://github.com/casey/just
[rustup]: https://www.rust-lang.org/tools/install
[kaggle]: https://www.kaggle.com/datasets/joonasyoon/file-format-detection
