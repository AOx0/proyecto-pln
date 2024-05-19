import subprocess
import os

# Obtenido de https://github.com/helix-editor/helix/blob/master/languages.toml
LANGS = [
    ("C", [("/*", "*/")], ["//"]),
    ("C#", [("/*", "*/")], ["//"]),
    ("C++", [("/*", "*/")], ["//"]),
    ("Clojure", [], [";"]),
    ("CSS", [("/*", "*/")], []),
    # ("CSV", [], []),
    ("Dart", [("/*", "*/")], ["//"]),
    ("Diff", [], ["#"]),
    ("Elixir", [], ["#"]),
    ("Erlang", [], ["%%"]),
    ("GAS", [("/*", "*/")], ["#", ";"]),
    ("GLSL", [("/*", "*/")], ["//"]),
    ("Go", [("/*", "*/")], ["//"]),
    # ("Graphviz (DOT)", [], []),
    ("HTML", [("<!--", "'-->'")], []),
    ("Java", [("/*", "*/")], ["//"]),
    ("Javascript", [("/*", "*/")], ["//"]),
    ("JSON", [], ["//"]),
    ("Julia", [("#=", "=#")], ["#"]),
    ("Jupyter Notebook", [], ["#"]),
    ("Kotlin", [("/*", "*/")], ["//"]),
    ("Less", [], []),
    ("Lisp", [], [";"]),
    ("Lua", [("'--[['", "'--]]'")], ["'--'"]),
    ("Makefile", [], ["#"]),
    ("Markdown", [("<!--", "'-->'")], []),
    ("PHP", [("/*", "*/")], ["//"]),
    ("PowerShell", [("<#", "#>")], ["#"]),
    ("Python", [], ["#"]),
    ("Q#", [], ["//"]),
    ("Ruby", [("=begin", "=end")], ["#"]),
    ("Rust", [("/*", "*/")], ["//"]),
    ("Scheme", [], [";"]),
    ("Shell", [], ["#"]),
    ("SQL", [("/*", "*/")], ["'--'"]),
    ("SVG", [("<!--", "'-->'")], []),
    ("Text", [], []),
    ("XML", [("<!--", "'-->'")], []),
    ("YAML", [], ["#"]),
]

faulty = "/home/ae/repos/archivos/dataset/Dart/023343.dart"
if os.path.exists(faulty):
    print(f"Removing {faulty}")
    os.remove(faulty)


for lang, multi, single in LANGS:
    command = ["cleaner", f"/home/ae/repos/archivos/dataset2/{lang}"]
    for open, close in multi:
        command += ["--open", open, "--close", close]
    for single in single:
        command += ["--single-line", single]

    if len(command) > 2:
        print(f"Exec {command}")
        subprocess.run(command)
