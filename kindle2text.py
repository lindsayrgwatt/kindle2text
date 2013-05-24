# To get your Kindle highlights:
# http://stackoverflow.com/questions/2184862/saving-the-manipulated-dom-html-after-editing-it-with-firebug

from bs4 import BeautifulSoup
from bs4.element import NavigableString
from bs4.element import Tag

SOURCE = "/Users/lindsayrgwatt/apps/kindle2text/recent_highlights.html"

entries = open(SOURCE, 'r')
soup = BeautifulSoup(entries)

highlights = {} # {'book title':[highlight1, highlight2]}
current_book = {}

# Each book starts with a div with class"bookMain"
first_title = soup.find("div", class_="bookMain")
current_book = {
    'title':first_title.find("a").string,
    'highlights':[]
}

counter = 0
# Alas, Amazon made every highlight and book siblings of each other; highlights are not children of books
for sibling in first_title.next_siblings:
    # In a document, the siblings will be of two types:
    # NavigableString - typically a newline character
    # Tag - the actual BeautifulSoup tag you can iterate over
    
    if isinstance(sibling, Tag):
        if 'bookMain' in sibling['class']:
            # Promote current book to highlights
            highlights[current_book['title']] = current_book['highlights']
            # Reset current book
            current_book = {
                'title':sibling.find("a").string,
                'highlights':[]
            }
        else:
            highlight = sibling.find("span", class_="highlight")
            if highlight and highlight.string:
                current_book['highlights'].append(highlight.string+"\n")
            else:
                print "Something else here"


# Promote last book
highlights[current_book['title']] = current_book['highlights']

books = highlights.keys()

for book in books:
    print "\n"
    print book
    print "\n"
    
    highlighted = highlights[book]
    for highlight in highlighted:
        print highlight
    
    print "\n"
    print "\n"
    print "============================================================================"
