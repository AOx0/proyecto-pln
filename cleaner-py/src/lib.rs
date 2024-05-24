use bstr::BStr;
use cleaner_lib::{
    delimit::{Delimiter, Multiline},
    lexer::Section,
};
use pyo3::prelude::*;

type Singles = Vec<&'static str>;
type Multis = Vec<(&'static str, &'static str)>;

#[pyfunction]
fn lang(lang: &str) -> PyResult<Option<(Multis, Singles)>> {
    let lang = lang.trim().to_lowercase();

    let res = match lang.as_str() {
        "c" => (vec![("/*", "*/")], vec!["//"]),
        "c#" => (vec![("/*", "*/")], vec!["//"]),
        "c++" => (vec![("/*", "*/")], vec!["//"]),
        "clojure" => (vec![], vec![";"]),
        "css" => (vec![("/*", "*/")], vec![]),
        "dart" => (vec![("/*", "*/")], vec!["//"]),
        "diff" => (vec![], vec!["#"]),
        "elixir" => (vec![], vec!["#"]),
        "erlang" => (vec![], vec!["%%"]),
        "gas" => (vec![("/*", "*/")], vec!["#", ";"]),
        "glsl" => (vec![("/*", "*/")], vec!["//"]),
        "go" => (vec![("/*", "*/")], vec!["//"]),
        "html" => (vec![("<!--", "-->")], vec![]),
        "java" => (vec![("/*", "*/")], vec!["//"]),
        "javascript" => (vec![("/*", "*/")], vec!["//"]),
        "json" => (vec![], vec!["//"]),
        "julia" => (vec![("#=", "=#")], vec!["#"]),
        "jupyter notebook" => (vec![], vec!["#"]),
        "kotlin" => (vec![("/*", "*/")], vec!["//"]),
        "less" => (vec![], vec![]),
        "lisp" => (vec![], vec![";"]),
        "lua" => (vec![("--[[", "--]]")], vec!["--"]),
        "makefile" => (vec![], vec!["#"]),
        "markdown" => (vec![("<!--", "-->")], vec![]),
        "php" => (vec![("/*", "*/")], vec!["//"]),
        "powershell" => (vec![("<#", "#>")], vec!["#"]),
        "python" => (vec![], vec!["#"]),
        "q#" => (vec![], vec!["//"]),
        "ruby" => (vec![("=begin", "=end")], vec!["#"]),
        "rust" => (vec![("/*", "*/")], vec!["//"]),
        "scheme" => (vec![], vec![";"]),
        "shell" => (vec![], vec!["#"]),
        "sql" => (vec![("/*", "*/")], vec!["--"]),
        "svg" => (vec![("<!--", "-->")], vec![]),
        "text" => (vec![], vec![]),
        "xml" => (vec![("<!--", "-->")], vec![]),
        "yaml" => (vec![], vec!["#"]),
        _ => return Ok(None),
    };

    Ok(Some(res))
}

#[pyfunction]
fn string(
    s: &str,
    multi: Option<Vec<(&str, &str)>>,
    single: Option<Vec<&str>>,
) -> PyResult<String> {
    let multis = multi.unwrap_or_default();
    let multis: Vec<Multiline> = {
        multis
            .iter()
            .map(|(o, c)| Multiline::new(o, c).unwrap())
            .collect()
    };

    let singles = single.unwrap_or_default();
    let singles: Vec<Delimiter> = {
        singles
            .iter()
            .map(|s| Delimiter(s.as_bytes().into()))
            .collect()
    };

    if multis.is_empty() && singles.is_empty() {
        return Ok(s.to_string());
    }

    let contents = BStr::new(s.as_bytes());
    let lexer = cleaner_lib::lexer::Lexer::new(contents, &multis, &singles).unwrap();

    let iter_clean = lexer.into_iter().map(|e| match e {
        Section::Raw(str) => std::borrow::Cow::Borrowed(str),
        Section::DelimOpen(delim) => std::borrow::Cow::Borrowed(delim),
        Section::DelimSingle(delim) => std::borrow::Cow::Borrowed(delim),
        Section::DelimClose(delim) => std::borrow::Cow::Borrowed(delim),
    });

    let mut res = String::with_capacity(s.len());

    for clean in iter_clean {
        res.push_str(std::str::from_utf8(&clean).unwrap_or_default())
    }

    Ok(res)
}

/// A Python module implemented in Rust.
#[pymodule]
fn _cleaner(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(string, m)?)?;
    m.add_function(wrap_pyfunction!(lang, m)?)?;
    Ok(())
}
