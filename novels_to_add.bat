@ECHO OFF

FOR /F %%G in (novels_to_add.txt) DO novelsave process --threads 1 %%G