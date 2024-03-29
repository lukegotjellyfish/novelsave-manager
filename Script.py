# -*- coding: utf-8 -*-

import re
import sqlite3
import subprocess
import time
import requests
import os
from ast import literal_eval
from datetime import datetime, timezone
from bs4 import BeautifulSoup


def decode_novelsave_output(value):
    try:
        value = value.decode("utf-8", 'ignore')
    except AttributeError:
        value = value[0].decode("utf-8", 'ignore')
    return value


def update_novel_covers():
    # TODO Add novel cover ids to novelsave's database so when they are packed they are added

    #db = sqlite3.connect("C:/Users/Lukeg/AppData/Local/Mensch272/novelsave/data.sqlite")
    db = sqlite3.connect("/root/.config/novelsave/data.sqlite")
    dbCursor = db.cursor()
    dbCursor.execute("SELECT url, novel_id FROM novel_urls")
    novel_entry_list = list(dbCursor.fetchall())

    for novel_entry in novel_entry_list:
        novelsave_id = novel_entry[1]

        my_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
        url = novel_entry[0]

        r = requests.get(url, headers=my_headers)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')

        # ScribbleHub: [0] https://cdn.scribblehub.com/images/3/immortal-only-accepts-female-disciples_77292_1642732345.jpg
        # NovelPub:    [1] https://static.novelpub.com/bookcover/300x400/00848-regressor-instruction-manual.jpg
        # NovelFull:    + [1]
        # https://novelfull.com/uploads/thumbs/war-sovereign-soaring-the-heaven-e5fb421bc4-2239c49aee6b961904acf173b7e4602a.jpg

        novel_cover = soup.find_all('img')
        """ Sources:
         - boxnovel.com
         - novelfull.com
         - readnovelfull.com
         - novelpub.com
         - scribblehub.com
        """

        if "scribblehub" in url:
            novel_cover = str(novel_cover[0].get('src'))
        elif "novelpub" in url:
            novel_cover = str(novel_cover[1].get('src'))
        elif ("allnovelfull" in url) or ("readnovelfull" in url):
            novel_cover = str(novel_cover[1].get('src'))
        elif "novelfull" in url:
            novel_cover = f"https://novelfull.com{novel_cover[1].get('src')}"
        else:
            # Give up
            continue

        novel_cover_data = requests.get(novel_cover, headers=my_headers).content

        # appdata_path = os.getenv('APPDATA').replace('\\', '/')[:-8]
        try:
            #os.mkdir(f'{appdata_path}/Local/Mensch272/novelsave/data/{novelsave_id}/')
            os.mkdir(f'/root/.config/novelsave/data/{novelsave_id}/')
        except FileExistsError:
            pass
        #with open(f'{appdata_path}/Local/Mensch272/novelsave/data/{novelsave_id}/cover.jpg', 'wb') as nc:
        with open (f'/root/.config/novelsave/data/{novelsave_id}/cover.jpg', 'wb') as nc:
            print(f"Downloading Novel Cover (ID: {novelsave_id}) : {novel_cover}")
            nc.write(novel_cover_data)


class Database:
    db = None
    db_path = "Novel_Database.db"
    dbCursor = None

    novel_library_path = ""

    def __init__(self, db_path):
        self.db_path = db_path
        self.db = sqlite3.connect(self.db_path)
        self.dbCursor = self.db.cursor()

        create_table = """CREATE TABLE IF NOT EXISTS
        Novels(
            novel_id INTEGER, 
            novel_title TEXT UNIQUE,
            novel_author TEXT,
            novel_chapters INTEGER, 
            novel_url TEXT, 
            novel_biography TEXT,
            novel_path TEXT,
            novelsave_id INTEGER,
            novel_modified_date INTEGER,
            PRIMARY KEY(novel_id AUTOINCREMENT)
        )
        """
        self.dbCursor.execute(create_table)

        # stdout = subprocess.Popen("novelsave config show", stdout=subprocess.PIPE).communicate()

    def add_new_novel_to_db(self, novel_url_check="", update=False):
        # Validate URL
        # ======================================
        if novel_url_check == "":
            novel_url_check = input("Novel URL: ")

        # Get stdout and stderr from completed novelsave process command
        # process Updates the novel if it already exists
        process_stdout, process_stderr = subprocess.Popen(f"novelsave process {novel_url_check}",
                                                          stdout=subprocess.PIPE,
                                                          stderr=subprocess.PIPE).communicate()
        # If error
        if process_stderr != (None, b''):
            return False
        # =======================================
        print()

        result = self.add_novel_to_db(novel_url_check, update)
        if result is True:
            return True
        else:
            return False

    def update_novels(self, package=False):
        try:
            max_novelsave_id = subprocess.Popen(f"novelsave list",
                                                stdout=subprocess.PIPE).communicate()
            max_novelsave_id = decode_novelsave_output(max_novelsave_id).split("\n")[:-1][-1]
            max_novelsave_id = int(re.search("\\|.*[^0-9]([0-9][0-9][0-9]|[0-9][0-9]|[0-9]).*[^\\|]\\|.*[^a-z][a-z]",
                                             max_novelsave_id).group(1)) + 1
        except IndexError:
            max_novelsave_id = 1000

        if package == False:
            print("\nUpdating Novels")
        else:
            print("\nPackaging Novels")
        for x in range(1, max_novelsave_id):
            if package == False:
                result = self.add_novel_to_db(x, update=True)
                if result is False:
                    print()
                    break
            else:
                subprocess.Popen(f"novelsave package {x}",
                                 stdout=subprocess.PIPE).communicate()
                print(f"Packaged NovelSave ID {x}")
        print()

    def add_novel_to_db(self, novel_url_or_id, update=False):
        while True:
            info_stdout = subprocess.Popen(f"novelsave info {novel_url_or_id}",
                                           stdout=subprocess.PIPE).communicate()

            # Example output:
            # ['[novel]',
            # 'id = 5',
            # "title = 'A Chance To Become An Adonis'",
            # "author = 'placeintime'",
            # "lang = 'en'",
            # "thumbnail = 'https://cdn.scribblehub.com/images/8/A-Chance-To-Become-A-Adonis_179849_1601687179.jpg'",
            # 'synopsis = [\'Laying in his own pool of blood, Lu Chen watches his wife being embraced by another man. He cou
            # ldn’t believe it. If there is any way possible, Lu Chen wanted to tear them apart from each other, yet nothing
            # . Lu Chen couldn’t do anything as he slowly dies. And the final words he will ever hear was,\', \'“You will al
            # ways be nothing but second place.” Then a bullet went through his chest.\', \'Before Lu Chen had lost all cons
            # ciousness, endless regret begins to flow through him. The people that cared for him he ignored, people that tr
            # usted him he betrayed. The only thing he had on his mind was; a second chance.\', "However, it is as if somebo
            # dy had heard him plead. Lu Chen was sent back to his 18-year-old body. He didn\'t want to believe it, yet he h
            # ad to. Lu Chen couldn\'t waste this opportunity. What will the young man do to change his future?", \'Hello gu
            # ys. I will be posting 2 chapters every 2 days somewhere between 9:00-10:00 pm.\', \'(This novel is all rights
            # reserved)\', \'Discord link: https://discord.gg/Ge8JfDk33C\', \'Please note that I will be posting on RoyalRoa
            # d and Webnovel as well.\']',
            # "urls = ['https://www.scribblehub.com/series/179849/a-chance-to-become-an-adonis/']",
            # '',
            # '[chapters]',
            # 'total = 411',
            # 'downloaded = 411',
            # '']
            info_output = decode_novelsave_output(info_stdout)

            # If Novel not found in novelsave database, try to add it
            if "Novel not found" in info_output:
                result = self.add_new_novel_to_db(novel_url_or_id)
                if result is False:
                    return False
                else:
                    break
            else:
                break

        info_output = info_output.split("\r\n")

        novelsave_id = info_output[1].replace("id = ", "")
        novel_title = info_output[2].replace("title = ", "").replace("'", "")
        novel_author = info_output[3].replace("author = ", "").replace("'", "")
        novel_chapters = info_output[11].replace("downloaded = ", "")
        novel_url = literal_eval(info_output[7].replace("urls = ", ""))[0]
        novel_source = ""
        if "novelfull" in novel_url:
            novel_source = "NovelFull"
        if "novelpub" in novel_url:
            novel_source = "NovelPub"
        if "scribble" in novel_url:
            novel_source = "Scribble Hub"
        novel_biography = '\n'.join(literal_eval(info_output[6].replace("synopsis = ", "")))
        novel_path = f"{self.novel_library_path}/{novel_source}/{novel_title}/{novel_title}.epub"
        novel_modified_date = int(round(datetime.now(timezone.utc).timestamp(), 0))

        # Try to add the novel details to the database
        while True:
            # Attempt SQL Execution
            try:
                new_novel_chapters = 0
                self.dbCursor.execute("SELECT * FROM Novels WHERE novel_title = ?", (novel_title,))
                novel_entry = self.dbCursor.fetchall()
                if len(novel_entry) == 0:
                    update = False
                else:
                    new_novel_chapters = str(novel_entry[0][3])

                if update is False:
                    self.dbCursor.execute("INSERT INTO Novels VALUES (NULL,?,?,?,?,?,?,?,?)",
                                          (novel_title, novel_author, novel_chapters, novel_url,
                                           novel_biography, novel_path, novelsave_id, novel_modified_date))
                elif new_novel_chapters != novel_chapters:
                    result = self.dbCursor.execute("""UPDATE Novels 
                                             SET novel_chapters = ?, novel_modified_date = ?
                                             WHERE novel_title = ? AND novel_chapters != ?""",
                                                   (novel_chapters, novel_modified_date, novel_title, novel_chapters))
                    print(
                        f'Updated "{novel_title}" (ID: {novelsave_id}), |{new_novel_chapters}| chapters to |{novel_chapters}| chapters')
                else:
                    print(f'No Updates for "{novel_title}" (ID: {novelsave_id})')
                # Can't account for chapter list actually updating unless I do a SELECT call
                #  so I've commented out the message to the user

                # No errors, break
                break
            # If the database is locked, inform user then delay one second
            except sqlite3.OperationalError as err:
                print(f"Database Error Message: {err}")
                time.sleep(1)
            # If the novel title already exists in the database...
            except sqlite3.IntegrityError as err:
                if update is False:
                    print(f"Database Error Message: {err}")
                    # If input is novelsave id
                    if type(novel_url_or_id) is int:
                        # Add id to the novel title to show user
                        novel_title += f" | {novel_url_or_id}"
                    # Tell user that the novel is already in the database
                    print(f"Novel ({novel_title} | {novel_url}) caused integrity Error (Duplicate Title?)\n")
                # return True as it is already in the database
                return True

        # Novel Title is unique, commit the changes to save the row to the database
        self.db.commit()

        # Print "added <novel>" to confirm the novel has been added to the database
        if update == False:
            print(f'Added "{novel_title}" (ID: {novelsave_id}) to novel database')
        # Novel has been added to the database, return True
        return True


def main():
    database = Database("Novel_Database.db")
    database.novel_library_path = "G:/Books/Novels/novelsave"

    while True:
        #novelsave_config_show = str(subprocess.Popen(f"novelsave config show", stdout=subprocess.PIPE).communicate())
        #novel_ex_path = re.search(r"value=('.*[^']')", novelsave_config_show).group(1)
        #print(f"Current Novel Export Path: {novel_ex_path}")

        print("[1] Add Novel\n" +
              "[2] Update/Add novelsave Novels\n" +
              "[3] Set Novel Export Path\n" +
              "[4] List Novels\n" +
              "[5] Update Novel Covers\n" +
              "[6] Package Novels")

        try:
            result = int(input(f"Select Function: "))
        except ValueError:
            continue
        if result == 1:
            database.add_new_novel_to_db()
        if result == 2:
            database.update_novels()
        if result == 3:
            print()
            path = "G:/Books/Novels/novelsave"
            subprocess.Popen("novelsave config set novel.dir --value G:/Books/Novels/novelsave").communicate()
            database.novel_library_path_path = path
            print()
        if result == 4:
            print()
            subprocess.Popen("novelsave list").communicate()
            print()
        if result == 5:
            update_novel_covers()
        if result == 6:
            database.update_novels(package=True)


if __name__ == '__main__':
    main()
