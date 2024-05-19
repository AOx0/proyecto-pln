mod args;
mod log;

use clap::Parser as _;
use cleaner_lib::{
    delimit::{Delimiter, Multiline},
    lexer::{Lexer, Section},
};
use itertools::{izip, Itertools};
use tokio::io::AsyncReadExt;

#[tokio::main]
async fn main() -> std::process::ExitCode {
    let args::Args {
        path,
        open,
        close,
        max_open_files,
        single_line,
    } = args::Args::parse();

    info!("Replacing values at {:?}", path.display());

    if open.len() != close.len() {
        error!("Invalid delimiter pairs",);
        return std::process::ExitCode::FAILURE;
    }

    let multilines = izip!(&open, &close)
        .map(|(o, c)| Multiline::new(o, c).unwrap())
        .collect_vec();
    let singleline = single_line
        .iter()
        .map(|d| Delimiter::from(d.as_str().trim_matches('\'')))
        .collect_vec();

    let semaphore = tokio::sync::Semaphore::new(max_open_files);

    let rep_multi = std::sync::atomic::AtomicUsize::new(0);
    let rep_single = std::sync::atomic::AtomicUsize::new(0);
    let num_files = std::sync::atomic::AtomicUsize::new(0);

    let inc_multi = || {
        rep_multi.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
    };
    let inc_sing = || {
        rep_single.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
    };

    async_scoped::TokioScope::scope_and_block(|s| {
        for entry in walkdir::WalkDir::new(path).max_open(10).into_iter() {
            let res = || async {
                let guard = semaphore.acquire().await;

                let entry = match entry {
                    Ok(entry) => entry,
                    Err(err) => {
                        warn!("Error with entry: {:?}", err);
                        return std::process::ExitCode::FAILURE;
                    }
                };

                if !entry.file_type().is_file() {
                    return std::process::ExitCode::FAILURE;
                }

                num_files.fetch_add(1, std::sync::atomic::Ordering::Relaxed);

                let file = tokio::fs::OpenOptions::new()
                    .read(true)
                    .create(false)
                    .open(entry.path())
                    .await;

                let mut file = match file {
                    Ok(file) => file,
                    Err(err) => {
                        warn!("Error with entry {:?}: {:?}", entry.path().display(), err);
                        return std::process::ExitCode::SUCCESS;
                    }
                };

                let mut contents = Vec::new();
                if let Err(err) = file.read_to_end(&mut contents).await {
                    warn!("Error reading {:?}: {:?}", entry.path().display(), err);
                    return std::process::ExitCode::SUCCESS;
                };

                let lexer = Lexer::new(&contents, &multilines, &singleline).unwrap();

                let res = iter_clean(lexer, &inc_multi, &inc_sing);

                let mut target = tokio::fs::OpenOptions::new()
                    .truncate(true)
                    .create(true)
                    .write(true)
                    .open(entry.path())
                    .await
                    .unwrap();

                cleaner_lib::lexer::write_to_file(res, &mut target)
                    .await
                    .unwrap();

                drop(guard);

                std::process::ExitCode::SUCCESS
            };

            s.spawn(res())
        }
    });

    info!(
        "Performed on {} files: 
      - {} multiline replacements
      - {} single line replacements",
        num_files.load(std::sync::atomic::Ordering::Relaxed),
        rep_multi.load(std::sync::atomic::Ordering::Relaxed),
        rep_single.load(std::sync::atomic::Ordering::Relaxed),
    );
    std::process::ExitCode::SUCCESS
}

fn iter_clean<'s>(
    replacer: Lexer<'s>,
    on_open: &'s impl Fn(),
    on_close: &'s impl Fn(),
) -> impl Iterator<Item = std::borrow::Cow<'s, bstr::BStr>> {
    replacer.into_iter().filter_map(|e| match e {
        Section::Raw(str) => Some(std::borrow::Cow::Borrowed(str)),
        Section::DelimOpen(_) => {
            on_open();
            None
        }
        Section::DelimSingle(_) => {
            on_close();
            None
        }
        Section::DelimClose(_) => None,
    })
}
