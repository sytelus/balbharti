import shutil
import pathlib
import os

pdf_folder = r'e:\balbharti'
metadata_text = pathlib.Path('balbharty_metadata.csv').read_text(encoding='utf-8')
dictionary_text = pathlib.Path('dictionary_gpt.txt').read_text(encoding='utf-8')
translation = {}

languages = set(['Marathi', 'Hindi', 'English', 'Urdu', 'Gujarati', 'Kannada', 'Sindhi(Are)', 'Sindhi(Dev)'])

for line in dictionary_text.splitlines():
    if not line:
        continue
    words = line.split('\t')
    translation[words[0]] = words[1]
    translation['(' + words[0]] = '(' + words[1]
    translation[words[0] + ')'] = words[1] + ')'
    translation['(' + words[0] + ')'] = '(' + words[1] + ')'


lines = metadata_text.splitlines()
filename_map = {}
for line in lines[1:]:
    if not line:
        continue
    title, cover, pdf_url, filename = line.split(',')
    filename = filename.replace('"', '')

    # translate title
    parts = title.split()
    grade = parts[0]+' '+parts[1]
    grade = translation[grade]
    language = parts[-1]
    language = translation[language]

    rest = [translation[word] for word in parts[2:-1]]
    title = ' '.join([grade] + rest + [language])

    filename_map[filename] = (title, grade, language)

for i in range(1, 1170):
    filename = f'{i}.pdf'
    filepath = os.path.join(pdf_folder, filename)
    if os.path.exists(filepath):
        title, grade, language = filename_map[filename]
        os.makedirs(os.path.join(pdf_folder, language, grade), exist_ok=True)
        shutil.move(filepath, os.path.join(pdf_folder, language, grade, title+'.pdf'))
