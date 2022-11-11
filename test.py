import sqlite3
import requests
import os
from bs4 import BeautifulSoup

db = sqlite3.connect("Novel_Database.db")
dbCursor = db.cursor()

dbCursor.execute("SELECT novel_url, novelsave_id FROM Novels")
novel_entry_list = list(dbCursor.fetchall())

for novel_entry in novel_entry_list:
    novelsave_id = novel_entry[1]

    my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    url = novel_entry[0]
    r = requests.get(url,headers=my_headers)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')


    # ScribbleHub: [0] https://cdn.scribblehub.com/images/3/immortal-only-accepts-female-disciples_77292_1642732345.jpg
    # NovelPub:    [1] https://static.novelpub.com/bookcover/300x400/00848-regressor-instruction-manual.jpg
    # NovelFull:   https://novelfull.com + [1]
    # https://novelfull.com/uploads/thumbs/war-sovereign-soaring-the-heaven-e5fb421bc4-2239c49aee6b961904acf173b7e4602a.jpg

    novel_cover = soup.find_all('img')
    if "scribblehub" in url:
        novel_cover = str(novel_cover[0].get('src'))
    elif "novelpub" in url:
        novel_cover = str(novel_cover[1].get('src'))
    elif "novelfull" in url:
        novel_cover = f"https://novelfull.com{novel_cover[1].get('src')}"

    print(f"Novel Cover: {novel_cover}")

    novel_cover_data = requests.get(novel_cover,headers=my_headers).content
    os.mkdir(f'C:/Users/Lukeg/AppData/Local/Mensch272/novelsave/data/{novelsave_id}/')
    with open(f'C:/Users/Lukeg/AppData/Local/Mensch272/novelsave/data/{novelsave_id}/cover.jpg', 'wb') as nc:
        nc.write(novel_cover_data)