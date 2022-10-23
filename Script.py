import sqlite3
import os
import glob
from ahk import AHK


class Database:
    novel_library_path = ""

    def __init__(self, value):
        self.db = value
        self.dbCursor = value.cursor()


def scan_novels(database):
    for folder in os.listdir(database.novel_library_path):
        for novel in os.listdir(f"{database.novel_library_path}/{folder}"):
            print(novel)


def update_novels():
    pass


def add_novel():
    pass


def export_novel_links():
    #https://www.novelupdates.com/?s=FIRSTWORD+SECONDWORD
    pass


def main():
    ahk.win_get("C:\Windows\System32\cmd.exe - lncrawl")
    database = Database(sqlite3.connect("Novel_Database.db"))
    database.novel_library_path = "G:/Books/Novels/Lncrawl/Lightnovels"

    while True:
        print("[1] - Scan lightnovel-crawler path\n" +
              "[2] - Update Novels\n" +
              "[3] - Add Novel\n" +
              "[4] - Export Novel Links")
        result = int(input(f"Select Function: "))

        if result == 1:
            scan_novels(database)
        if result == 2:
            update_novels()
        if result == 3:
            add_novel()
        if result == 4:
            export_novel_links()


if __name__ == '__main__':
    main()

# path = "G:/Books/Novels/Lncrawl/Lightnovels/"
# result=subprocess.check_output("", shell=True)
