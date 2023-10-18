import requests
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
import os

# Define Constants
BASE_URL = 'https://books.ebalbharati.in/archives/Books/{}.pdf'
DIRECTORY = 'downloaded_pdfs'
LOG_FILE = 'download_status.log'
HTML_FILE = 'index.html'
MAX_INDEX = 1200

# Check if directory exists
if not os.path.exists(DIRECTORY):
    os.mkdir(DIRECTORY)

# Check for log file
starting_index = 1
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'r') as log:
        lines = log.readlines()
        if lines:
            last_url = lines[-1].split('\t')[1].strip()
            starting_index = int(last_url.split('/')[-1].split('.')[0]) + 1

with open(LOG_FILE, 'a') as log:
    for index in range(starting_index, MAX_INDEX):
        url = BASE_URL.format(index)
        response = requests.get(url, stream=True)

        log.write(f"{response.status_code}\t{url}\n")

        # Only process if successful
        if response.status_code == 200:
            file_path = os.path.join(DIRECTORY, f'{index}.pdf')
            with open(file_path, 'wb') as pdf_file:
                for chunk in response.iter_content(chunk_size=8192):
                    pdf_file.write(chunk)

            # # Extract first page as jpg
            # images = convert_from_path(file_path, first_page=1, last_page=1)
            # image_path = os.path.join(DIRECTORY, f'pg1_{index}.jpg')
            # images[0].save(image_path, 'JPEG')

            # # Extract text from second page using GPT-4 (here using pytesseract as an example)
            # # Extract first page as jpg
            # images = convert_from_path(file_path, first_page=2, last_page=2)
            # image_path = os.path.join(DIRECTORY, f'pg2_{index}.jpg')
            # images[0].save(image_path, 'JPEG')

# # Generate HTML file
# with open(HTML_FILE, 'w') as html:
#     html.write('<table>\n')
#     for index in range(1, 1201):
#         if os.path.exists(os.path.join(DIRECTORY, f'{index}.pdf')):
#             html.write(f'<tr>\n')
#             html.write(f'<td><img src="{DIRECTORY}/pg1_{index}.jpg" width="100" height="150"></td>\n')
#             with open(os.path.join(DIRECTORY, f'{index}.txt'), 'r') as txt_file:
#                 html.write(f'<td>{txt_file.read()}</td>\n')
#             html.write(f'<td><a href="{DIRECTORY}/{index}.pdf">Download</a></td>\n')
#             html.write(f'</tr>\n')
#     html.write('</table>\n')
