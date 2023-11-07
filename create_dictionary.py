import pathlib
import os

pdf_folder = r'e:\balbharty'
metadata_text = pathlib.Path('balbharty_metadata.csv').read_text(encoding='utf-8')
lines = metadata_text.splitlines()

words = set()

for line in lines[1:]:
    if not line:
        continue
    title, cover, pdf_url, filename = line.split(',')
    parts = title.split()
    grade = parts[0]+' '+parts[1]
    words.add(grade)
    for word in parts[2:]:
        words.add(word)

pathlib.Path('dictionary.txt').write_text('\n'.join(sorted(words)), encoding='utf-8')
