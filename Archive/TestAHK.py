import re
import threading
from ahk import AHK
from ahk.daemon import AHKDaemon
import time
import os
import clipboard
import sys


class Capture_To_Text:
    binary_path = ""


def wait_for_text(text):
    prev_clipboard = clipboard.paste()
    while clipboard.paste() == prev_clipboard:
        os.system(f'{Capture_To_Text.binary_path} --screen-rect "13 38 1161 788" --clipboard > nul 2> nul')
        time.sleep(0.100)
        cur_clipboard = clipboard.paste()
        if text in cur_clipboard:
            time.sleep(0.200)
            break


def open_cmd(cmd_command):
    os.system(cmd_command)


novel_library_path = "C:/Users/GarrusLaptop/Documents/Lightnovels/lncrawl_manager/"
novel_title = "Kidnapped Dragons"
cwd = os.path.dirname(sys.argv[0]).replace("\\", "/")
Capture_To_Text.binary_path = f"{cwd}/Capture2Text/Capture2Text_CLI.exe"

ahk_path = "C:/Program Files/AutoHotkey//AutoHotkeyU64.exe"
ahk = AHK(executable_path=ahk_path)
daemon = AHKDaemon(executable_path=ahk_path)
daemon.start()


download_new_novel = 'lncrawl --format epub --single --all -f -o G:/Books/Novels/Lncrawl/Lightnovels/lncrawl_manager/Kidnapped_Dragons -q "Kidnapped Dragons" --suppress'

lncrawl_arg = f'start /wait cmd /c lncrawl --format epub --single --all -f -o "{novel_library_path}{novel_title}/"'
t = threading.Thread(target=open_cmd,
                     name="cmd_thread",
                     args=[lncrawl_arg])
t.start()

ahk.win_wait(title="C:\\Windows\\system32\\cmd.exe", timeout=10)
lncrawl_window = ahk.win_get(title="C:\\Windows\\system32\\cmd.exe")

# Setup window position
lncrawl_window.move(x=0, y=0, width=1200, height=800)

wait_for_text("Enter novel page url or query novel")

lncrawl_window.send(f"{novel_title}")
time.sleep(1)
lncrawl_window.send("{ENTER}")
wait_for_text("Searching")
time.sleep(0.100)

# Wait for Novel selection screen
wait_for_text("Which one is your novel")

# Select first Novel result
lncrawl_window.send("{ENTER}")
time.sleep(0.200)

# Wait for source selection
wait_for_text("0. Back")

# Select first source
lncrawl_window.send("{DOWN}")
lncrawl_window.send("{ENTER}")

# Wait for download confirmation
wait_for_text("Change selection")

while True:
    try:
        os.system(f'{Capture_To_Text.binary_path} --screen-rect "13 38 1161 788" --clipboard > nul 2> nul')
        time.sleep(0.200)
        novel_chapters = clipboard.paste()
        print(f"Regex search on: {novel_chapters}")
        novel_chapters = re.search(r"(((\d\d\d\d)|(\d\d\d)|\d\d|\d) chapters)", novel_chapters).group(1)
        novel_chapters = novel_chapters.split(" ")[0]
        break
    except AttributeError:
        continue
print(f"novel_chapters: {novel_chapters}")


# Select continue
lncrawl_window.send("{ENTER}")


