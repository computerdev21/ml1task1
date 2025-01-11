import os
import requests
import re
import sys
from bs4 import BeautifulSoup  # Import BeautifulSoup


# function to get the html source text of the medium article
def get_page():
    global url

    # Ask the user to input the URL
    url = input("Enter url of a medium article: ")

    # handling possible error
    if not re.match(r'https?://medium.com/', url):
        print('Please enter a valid website, or make sure it is a medium article')
        sys.exit(1)

    # Send GET request
    res = requests.get(url)

    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


# function to remove all the html tags and replace some with specific strings
def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>": "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub('\<(.*?)\>', '', text)
    return text


def collect_text(soup):
    text = f'url: {url}\n\n'
    para_text = soup.find_all('p')
    for para in para_text:
        cleaned_text = clean(para.text)
        text += f"{cleaned_text}\n\n"
    return text


# function to save file in the current directory
def save_file(text):
    if not os.path.exists('./scraped_articles'):
        os.mkdir('./scraped_articles')
    name = url.split("/")[-1]
    fname = f'scraped_articles/{name}.txt'

    # Write to a file
    with open(fname, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f'File saved in directory {fname}')


if __name__ == '__main__':
    text = collect_text(get_page())
    save_file(text)
# Instructions to Run this python code
# Give url as https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7
