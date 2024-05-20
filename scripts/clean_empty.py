import subprocess

REPLACEMENTS = [
    (r"\r", ""),
    (r"\w{15,}", ""),
    ("\t{2,}", "\t"),
    ("\n{2,}", "\n"),
    (" {2,}", " ")
]

for orig, into in REPLACEMENTS:
    command = [
        "ruplacer", "--quiet", "--go",
        orig, into, "/home/ae/repos/archivos/dataset2/"
    ]

    print(f"Exec {command}")
    subprocess.run(command)

