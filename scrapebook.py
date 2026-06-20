import requests
import os,sys
from bs4 import BeautifulSoup
def scrape():

    if not os.path.exists("book_data"):
        os.mkdir("book_data")
    for i in range(1,376):
        n_url=-1
        bookfile = "book"+str(i)+".txt"
        if not os.path.isfile(bookfile):
            # skip if the list file doesn't exist
            continue

        # try reading as utf-8 first, fall back on cp1252 with replacement on errors
        try:
            infile = open(bookfile, 'r', encoding='utf-8')
        except UnicodeDecodeError:
            infile = open(bookfile, 'r', encoding='cp1252', errors='replace')

        with infile:
            for page in infile:
                url = page.strip()
                if url == "":
                    continue
                n_url += 1
                filename = "00" + '0'*(3-len(str(i))) + str(i) + '0'*(3-len(str(n_url))) + str(n_url) + ".utf8"
                if not os.path.isfile(os.path.join("book_data", filename)):
                    print(str(i) + "-->" + str(n_url))
                    resp = requests.get(url)
                    if resp.status_code == 200:
                        soup = BeautifulSoup(resp.text, 'html.parser')
                        # ensure output file is properly closed
                        with open(os.path.join("book_data", filename), 'a+', encoding='utf-8') as f:
                            for paras in soup.findAll("p"):
                                f.write(str(paras.get_text()))
scrape()
