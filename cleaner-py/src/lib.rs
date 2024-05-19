use bstr::{BStr, ByteSlice, ByteVec};
use cleaner_lib::{
    delimit::{Delimiter, Multiline},
    lexer::Section,
};
use pyo3::{prelude::*, types::PyBytes};

#[allow(dead_code)]
type Singles = Vec<&'static str>;
#[allow(dead_code)]
type Multis = Vec<(&'static str, &'static str)>;

#[allow(dead_code)]
type SinglesBytes = Vec<PyObject>;
#[allow(dead_code)]
type MultisBytes = Vec<(PyObject, PyObject)>;

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
fn lang_bytes(py: Python, lng: &str) -> PyResult<Option<(MultisBytes, SinglesBytes)>> {
    let val = lang(lng);

    let (multis, singles) = match val {
        Ok(Some((multis, singles))) => (multis, singles),
        Ok(None) => return Ok(None),
        Err(err) => return Err(err),
    };

    let multis = multis
        .into_iter()
        .map(|(a, b)| {
            (
                PyBytes::new(py, a.as_bytes()).into(),
                PyBytes::new(py, b.as_bytes()).into(),
            )
        })
        .collect();

    let singles = singles
        .into_iter()
        .map(|a| PyBytes::new(py, a.as_bytes()).into())
        .collect();

    Ok(Some((multis, singles)))
}

/// Clean the comments
#[pyfunction]
fn clean_string(
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

    let iter_clean = lexer.into_iter().filter_map(|e| match e {
        Section::Raw(str) => Some(std::borrow::Cow::Borrowed(str)),
        Section::DelimOpen(_) => None,
        Section::DelimSingle(_) => None,
        Section::DelimClose(_) => None,
    });

    let mut res = String::with_capacity(s.len());

    for clean in iter_clean {
        res.push_str(std::str::from_utf8(&clean).unwrap_or_default())
    }

    Ok(res)
}

#[pyfunction]
fn clean_bytes(
    py: Python,
    s: &[u8],
    multi: Option<Vec<(&[u8], &[u8])>>,
    single: Option<Vec<&[u8]>>,
) -> PyResult<PyObject> {
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
            .copied()
            .map(|s| Delimiter(s.as_bstr()))
            .collect()
    };

    if multis.is_empty() && singles.is_empty() {
        return Ok(pyo3::types::PyBytes::new(py, s).into());
    }

    let contents = BStr::new(s.as_bytes());
    let lexer = cleaner_lib::lexer::Lexer::new(contents, &multis, &singles).unwrap();

    let iter_clean = lexer.into_iter().filter_map(|e| match e {
        Section::Raw(str) => Some(std::borrow::Cow::Borrowed(str)),
        Section::DelimOpen(_) => None,
        Section::DelimSingle(_) => None,
        Section::DelimClose(_) => None,
    });

    let mut res = Vec::with_capacity(s.len());

    for clean in iter_clean {
        res.push_str(clean.as_bstr())
    }

    Ok(pyo3::types::PyBytes::new(py, &res).into())
}

/// A Python module implemented in Rust.
#[pymodule]
fn ccleaner(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(clean_string, m)?)?;
    m.add_function(wrap_pyfunction!(clean_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(lang, m)?)?;
    m.add_function(wrap_pyfunction!(lang_bytes, m)?)?;
    Ok(())
}
