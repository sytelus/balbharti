import pathlib
import os

pdf_folder = r'e:\balbharty'
metadata_text = pathlib.Path('balbharty_metadata.csv').read_text(encoding='utf-8')
lines = metadata_text.splitlines()
filename_map = {}
for line in lines[1:]:
    if not line:
        continue
    title, cover, pdf_url, filename = line.split(',')
    filename = filename.replace('"', '')
    filename_map[filename] = title

for i in range(1, 1170):
    filename = f'{i}.pdf'
    filepath = os.path.join(pdf_folder, filename)
    if os.path.exists(filepath):
        title = filename_map[filename]
        os.rename(filepath, os.path.join(pdf_folder, f'{title}.pdf'))