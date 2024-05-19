use crate::delimit::{Delimiter, Multiline};
use anyhow::{anyhow, Result};
use bstr::BStr;
use std::borrow::Cow;
use tokio::io::AsyncWriteExt;

pub struct Lexer<'i> {
    pub source: &'i BStr,
    pub cursor: usize,
    pub in_comment: bool,
    pub multiline: &'i [Multiline<'i>],
    pub singleline: &'i [Delimiter<'i>],
}

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum Section<'i> {
    Raw(&'i BStr),
    DelimOpen(&'i BStr),
    DelimClose(&'i BStr),
    DelimSingle(&'i BStr),
}

impl<'i> Lexer<'i> {
    fn get_delimiter(&mut self) -> Option<Section<'i>> {
        let peek_delimiter = self.peek_delimiter(None);
        if let Some(delim) = peek_delimiter.map(|delim| match delim {
            Section::DelimOpen(s) | Section::DelimClose(s) | Section::DelimSingle(s) => s.len(),
            Section::Raw(_) => unreachable!("peek_delimiter does not return Raw"),
        }) {
            self.cursor += delim;
            peek_delimiter
        } else {
            None
        }
    }

    fn peek_delimiter(&self, offset: Option<usize>) -> Option<Section<'i>> {
        for indicator in self.multiline.iter() {
            let crate::delimit::Multiline(Delimiter(start), Delimiter(end)) = indicator;
            if !(self.remainder().len() >= start.len() || self.remainder().len() >= end.len()) {
                continue;
            }

            if self.offset(offset.unwrap_or_default()).starts_with(start) {
                return Some(Section::DelimOpen(start));
            } else if self.offset(offset.unwrap_or_default()).starts_with(end) {
                return Some(Section::DelimClose(end));
            }
        }

        for Delimiter(delimit) in self.singleline.iter() {
            if self.offset(offset.unwrap_or_default()).starts_with(delimit) {
                return Some(Section::DelimSingle(delimit));
            }
        }

        None
    }

    fn remainder(&self) -> &'i BStr {
        &self.source[self.cursor..]
    }

    fn offset(&self, offset: usize) -> &'i BStr {
        &self.source[self.cursor + offset..]
    }

    pub fn new(
        s: &'i [u8],
        multilines: &'i [Multiline<'i>],
        singleline: &'i [Delimiter<'i>],
    ) -> anyhow::Result<Self> {
        Ok(Lexer {
            in_comment: false,
            multiline: multilines,
            singleline,
            source: BStr::new(s),
            cursor: 0,
        })
    }
}

pub async fn write_to_file<'a>(
    iterator: impl Iterator<Item = Cow<'a, BStr>>,
    target: &mut tokio::fs::File,
) -> Result<()> {
    for r in iterator {
        let result = match r {
            Cow::Owned(slice) => target.write_all(&slice).await,
            Cow::Borrowed(slice) => target.write_all(slice).await,
        };

        result.map_err(|err| anyhow!("Error: {err}"))?
    }

    Ok(())
}

impl<'i> Iterator for Lexer<'i> {
    type Item = Section<'i>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.remainder().is_empty() {
            return None;
        }

        if !self.in_comment {
            match self.peek_delimiter(None) {
                Some(Section::DelimSingle(s)) => {
                    for i in 0..self.remainder().len() {
                        if self.offset(i).starts_with(b"\n") {
                            let _comment = &self.remainder()[..i];
                            self.cursor += i;

                            return Some(Section::DelimSingle(s));
                        }
                    }

                    self.cursor += self.remainder().len();
                    return Some(Section::DelimSingle(s));
                }
                Some(Section::DelimOpen(_)) => {
                    self.in_comment = true;
                    self.get_delimiter()
                }
                Some(Section::DelimClose(_)) => {
                    self.in_comment = false;
                    self.get_delimiter()
                }
                Some(Section::Raw(_)) => unreachable!("peek_delimiter does not return Raw"),
                None => {
                    for i in 0..self.remainder().len() {
                        match self.peek_delimiter(Some(i)) {
                            Some(Section::DelimOpen(_)) | Some(Section::DelimSingle(_)) => {
                                let raw = &self.remainder()[..i];
                                self.cursor += i;

                                return Some(Section::Raw(raw));
                            }
                            _ => (),
                        }
                    }

                    let rem_raw = &self.remainder();
                    self.cursor += rem_raw.len();

                    return Some(Section::Raw(rem_raw));
                }
            }
        } else {
            // If we are in a comment, we look for the closing tag
            let mut opened = 0;
            for i in 0..self.remainder().len() {
                let peek_delimiter = self.peek_delimiter(Some(i));
                match peek_delimiter {
                    Some(Section::DelimClose(_)) if opened == 0 => {
                        let _comment = &self.remainder()[..i];
                        self.in_comment = false;
                        self.cursor += i;

                        return self.get_delimiter();
                    }
                    Some(Section::DelimClose(_)) => {
                        opened -= 1;
                    }
                    Some(Section::DelimOpen(_)) => {
                        opened += 1;
                    }
                    _ => (),
                }
            }

            self.in_comment = false;
            Some(Section::Raw("".as_bytes().into()))
        }
    }
}

#[cfg(test)]
mod tests {
    use bstr::BStr;

    use crate::{
        delimit::{Delimiter, Multiline},
        lexer::Section,
    };

    use super::Lexer;

    #[test]
    fn lexer() {
        let contents =
            "/* Ajajaja esto es un comentario */ pub fn main() { return; /* Y esto igual */ } /*Ye/**/sto*/ // Ou\n // Ya";
        let delimiters = vec![Multiline::new("/*", "*/").unwrap()];

        let singles = vec![Delimiter::from("//")];
        let tokens: Vec<_> = Lexer::new(contents.as_bytes(), &delimiters, &singles)
            .unwrap()
            .collect();

        let expect = [
            Section::DelimOpen(BStr::new(b"/*")),
            Section::DelimClose(BStr::new(b"*/")),
            Section::Raw(BStr::new(b" pub fn main() { return; ")),
            Section::DelimOpen(BStr::new(b"/*")),
            Section::DelimClose(BStr::new(b"*/")),
            Section::Raw(BStr::new(b" } ")),
            Section::DelimOpen(BStr::new(b"/*")),
            Section::DelimClose(BStr::new(b"*/")),
            Section::Raw(BStr::new(b" ")),
            Section::DelimSingle(BStr::new(b"//")),
            Section::Raw(BStr::new(b"\n ")),
            Section::DelimSingle(BStr::new(b"//")),
        ];

        assert_eq!(expect.as_slice(), tokens.as_slice())
    }
}
