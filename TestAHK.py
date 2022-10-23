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
            break


def open_cmd(cmd_command):
    os.system(cmd_command)


novel_library_path = "G:/Books/Novels/Lncrawl/Lightnovels/lncrawl_manager/"
cwd = os.path.dirname(sys.argv[0]).replace("\\", "/")
Capture_To_Text.binary_path = f"{cwd}/Capture2Text/Capture2Text_CLI.exe"

ahk_path = "C:/Users/Lukeg/Desktop/AHK/AutoHotkeyU64.exe"
ahk = AHK(executable_path=ahk_path)
daemon = AHKDaemon(executable_path=ahk_path)
daemon.start()

t = threading.Thread(target=open_cmd, name="cmd_thread", args=["start /wait cmd /c lncrawl"])
t.start()

print("e")

ahk.win_wait(title="C:\\Windows\\system32\\cmd.exe", timeout=10)
lncrawl_window = ahk.win_get(title="C:\\Windows\\system32\\cmd.exe")

# Setup window position
lncrawl_window.move(x=0, y=0, width=1200, height=800)

wait_for_text("Enter novel page url or query novel")

novel_title = "Kidnapped Dragons"
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

# Wait for dir selection
wait_for_text("Enter output directory")

# Clear default directory
lncrawl_window.send("^u")
# Wait for line to be cleared
time.sleep(0.200)

# Input export directory
lncrawl_window.send(f"{novel_library_path}{novel_title}/")
lncrawl_window.send("{ENTER}")



