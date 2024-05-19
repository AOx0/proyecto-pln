#[derive(clap::Parser)]
pub struct Args {
    /// Where to look for replacing
    pub path: std::path::PathBuf,
    #[clap(long, short, value_delimiter = ' ', num_args = 1..)]
    /// Open delimiters
    pub open: Vec<String>,
    #[clap(long, short, value_delimiter = ' ', num_args = 1..)]
    /// Open delimiters
    pub close: Vec<String>,
    #[clap(long, short, value_delimiter = ' ', num_args = 1..)]
    /// Single line comment delimiter
    pub single_line: Vec<String>,
}
