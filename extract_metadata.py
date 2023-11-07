import pathlib

from bs4 import BeautifulSoup
import pandas as pd# Corrected extraction process

# Extract book details
book_details = []

html_content = pathlib.Path('metadata.html').read_text(encoding='utf-8')

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

for card in soup.find_all('div', class_='card shadow-sm text-center'):
    # Extract book title
    title = card.find('h5', class_='card-text mar').text.strip()

    # Extract book cover image source
    img_src = card.find('img')['src']

    # Extract book PDF download link from the onclick attribute of the button
    button = card.find('button')
    onclick_attr = button['onclick']

    # Properly extract the PDF URL from the onclick attribute string
    # Finding the actual URL between the escape quotes &quot;
    pdf_url_start = onclick_attr.find('&quot;') + 6  # Start index of the URL
    pdf_url_end = onclick_attr.find('&quot;', pdf_url_start)  # End index of the URL
    pdf_url = onclick_attr[pdf_url_start:pdf_url_end]

    # Append details to the list
    book_details.append({
        'Book Title': title,
        'Book Cover': img_src,
        'PDF URL': pdf_url
    })

# Create a DataFrame
books_df = pd.DataFrame(book_details)

# Display the DataFrame
print(books_df)

#books_df.to_csv('balbharty_metadata.csv', index=False)

books_df['Book Title'].to_csv('balbharty_titles.csv', index=False)
