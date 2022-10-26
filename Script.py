import sqlite3
import subprocess
import re

# valid_urls = [
#     "readnovelfull.com/",
#     "readlightnovels.net",
#     "readlightnovels.net",
#     "royalroad.com",
#     "readlightnovel.me",
#     "scribblehub.com",
#     "forums.spacebattles.com",
#     "forums.sufficientvelocity.com",
#     "wattpad.com",
#     "webnovel.com",
#
# ]

class Database:
    db = None
    db_path = "Novel_Database.db"
    dbCursor = None

    def __init__(self, db_path):
        self.db_path = db_path

    def init_database(self):
        self.db = sqlite3.connect(self.db_path)
        self.dbCursor = self.db.cursor()

        create_table = """CREATE TABLE IF NOT EXISTS
        Novels(
            novel_id INTEGER PRIMARY_KEY, 
            novel_title TEXT, 
            novel_chapters INTEGER, 
            novel_url TEXT, 
            novel_tags TEXT,
            novel_path TEXT
        )
        """
        self.dbCursor.execute(create_table)

        return self.db


def check_source(url):
    pass


def update_novels(database):
    pass


def add_novel(database1):
    # Validate URL
    # ======================================
    while True:
        novel_url_check = input("Novel URL: ")

        # TODO: Add following details into SQL insert command
        # result contains:
        #  the novel ID (for novelsave)
        #  the novel Title
        #  the number of chapters

        # Example output:
        # Novel not found: 'https://www.scribblehub.com/series/179849/a-chance-to-become-an-adonis/'.
        # Attempting to create new novel entry using url…
        # Retrieving novel information from https://www.scribblehub.com/series/179849/a-chance-to-become-an-adonis/…
        # Added new novel with values: id=5 title='A Chance To Become An Adonis' chapters=411.
        # Downloaded and saved thumbnail image to 5\cover.jpg (19.66 Kb).
        # Downloading 411 pending chapters with 16 threads…
        # Chapters download complete, 411 succeeded, with 0 errors.
        # Skipped assets download as none are pending.


        result = subprocess.Popen(f"novelsave process {novel_url_check}",
                                  stderr=subprocess.PIPE)

        # .communicate() waits for end
        if result.communicate() != (None, b''):
            break
    # =======================================

    # Package novel to epub
    print()

    # Example output:
    # Acquired 'A Chance To Become An Adonis' (5) from database.
    # Packaging to 'epub' succeeded and saved to '{novel.dir}/Scribble Hub\A Chance To Become An Adonis\A Chance To Become An Adonis.epub'.

    out, err = subprocess.Popen(f"novelsave package {novel_url_check} --target epub",
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if "ID_OR_URL" not in str(err):
        print(f"Added {novel_url_check} to novel database")
    else:
        print("Invalid URL")
    print()


def main():
    database = Database("Novel_Database.db")
    database.init_database()

    while True:
        novelsave_config_show = str(subprocess.Popen(f"novelsave config show", stdout=subprocess.PIPE).communicate())
        novel_ex_path = re.search(r"value=('.*[^']')", novelsave_config_show).group(1)
        print(f"Current Novel Export Path: {novel_ex_path}")
        print("[1] Add Novel\n" + "[2] Update Novels\n" + "[3] Set Novel Export Path\n")
        result = int(input(f"Select Function: "))

        if result == 1:
            add_novel(database)
        if result == 2:
            update_novels(database)
        if result == 3:
            print()
            subprocess.Popen("novelsave config set novel.dir --value G:/Books/Novels/novelsave").communicate()
            print()


if __name__ == '__main__':
    main()
