import requests
import re
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os.path

# Return a valid filename which not includes the invalid_char shown below
def valid_filename(name):
    invalid_char = [':', '\\', '/', '?', '*', '"', '>', '<', '|']
    valid_name_lst = list(name)

    for c in name:
        if c in invalid_char:
            valid_name_lst.remove(c)

    valid_name = ''.join(valid_name_lst)
    return valid_name

# Retreve images from network by urlretrieve
def parse_images(link):
    res = requests.get(link)
    soup = BeautifulSoup(res.text, 'html.parser')
    # Regular expression for all kinds of images
    image_tags = soup.find_all('a', {'href': re.compile('^https?://(i.)?(m.)?imgur.com')})

    # If there are images inside the post then download it
    if len(image_tags) > 0:
        global updated
        # Find out article's title to represent filename
        name = soup.find_all('span', {'class': 'article-meta-value'})[2].text
        filename = valid_filename(name)

        # If file exists then skip it
        if os.path.isfile('E:\\beauty\\{}_0.jpg'.format(filename)):
            updated = True
            return

        # Download images
        for index, tag in enumerate(image_tags):
            urlretrieve(tag['href'], 'E:\\beauty\\{}_{}.jpg'.format(filename, index))

# Retrieve valid post link
def parse_post_link(entry):
    global ptt_url

    if '(本文已被刪除)' in entry.find('div', 'title').text:
        post_link = None
    else:
        post_link = ptt_url + entry.find('div', 'title').find('a').get('href', None)
    return post_link

# PTT URL domain
ptt_url = 'https://www.ptt.cc'
# Home page of PTT beauty board
url = 'https://www.ptt.cc/bbs/beauty/index.html'
# Updated status
updated = False

while (not updated):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    post_entries = soup.find_all('div', {'class': 'r-ent'})

    for entry in post_entries:
        link = parse_post_link(entry)
        if link:
            parse_images(link)

    # Get the previous page (上一頁) 
    controls = soup('a', {'class': 'btn wide'})
    url = ptt_url + controls[1].get('href', None)
