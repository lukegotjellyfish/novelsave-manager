import sqlite3


class Database:
    def __init__(self, value):
        self.db = value
        self.dbCursor = value.cursor()

def scan_novels():
    pass


def update_novels():
    pass


def add_novel():
    pass


def export_novel_links():
    #https://www.novelupdates.com/?s=FIRSTWORD+SECONDWORD
    pass


def main():
    database = Database(sqlite3.connect("Novel_Database.db"))
    novel_library_path = "G:\Books\Novels\Lncrawl\Lightnovels"

    while True:
        print("[1] - Scan lightnovel-crawler path\n" +
              "[2] - Update Novels\n" +
              "[3] - Add Novel\n" +
              "[4] - Export Novel Links")
        result = input(f"Select Function: ")
        if result == 1:
            scan_novels()
        if result == 2:
            update_novels()
        if result == 3:
            add_novel()
        if result == 4:
            export_novel_links()

    while True:
        result = input(f"Enter Novel Title To add:" +
              f"")


if __name__ == '__main__':
    main()

# path = "G:/Books/Novels/Lncrawl/Lightnovels/"
# result=subprocess.check_output("", shell=True)
