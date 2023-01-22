# novelsave-manager
A Very WIP Script to manage the novelsave project for larger scale crawling and updating of ebooks.
Main feataures currently include:
 - Downloading book covers for novelsave (Bypassing 403 errors)
 - Updating/Packaging all novels in the novelsave database
 
 WIP Ideas that aren't implimented:
  - Swapping out the novelsave database to bypass database size and performance issues when many novels are added
  - Handling of novels that fail to download with novelsave
___
## Python Requirements
 - [novelsave](https://github.com/m-haisham/novelsave)
 - [novelsave-sources](https://github.com/m-haisham/novelsave_sources)
 - re
 - qlite3
 - subprocess
 - time
 - requests
 - os
 - ast
 - datetime
 - bs4
___
