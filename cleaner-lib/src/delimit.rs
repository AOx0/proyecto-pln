use anyhow::*;
use bstr::BStr;

#[derive(Clone, Copy)]
pub struct Multiline<'a>(pub Delimiter<'a>, pub Delimiter<'a>);

impl<'a> Multiline<'a> {
    #[allow(dead_code)]
    pub fn new<B: ?Sized + AsRef<[u8]>>(open: &'a B, close: &'a B) -> anyhow::Result<Self> {
        let open = BStr::new(open);
        let close = BStr::new(close);

        ensure!(
            open.len() >= 2,
            anyhow!("Open delimiter {open} does not have a len of 2 or more")
        );
        ensure!(
            close.len() >= 2,
            anyhow!("Close delimiter {close} does not have a len of 2 or more")
        );
        ensure!(
            open.is_ascii(),
            anyhow!("Open delimiters can only contain ASCII characters")
        );
        ensure!(
            close.is_ascii(),
            anyhow!("Close delimiters can only contain ASCII characters")
        );

        Ok(Self(Delimiter(open), Delimiter(close)))
    }
}

#[derive(Debug, Clone, Copy)]
pub struct Delimiter<'a>(pub &'a BStr);

impl<'a> From<&'a str> for Delimiter<'a> {
    fn from(value: &'a str) -> Self {
        Delimiter(BStr::new(value.as_bytes()))
    }
}

impl std::ops::Deref for Delimiter<'_> {
    type Target = BStr;

    fn deref(&self) -> &Self::Target {
        self.0
    }
}
