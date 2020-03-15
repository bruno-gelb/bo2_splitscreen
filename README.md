### purpose

run Borderlands 2 on PC with split screen for set number of players. Windows only.

### features

* support for multi-monitor configurations
* support for localized versions of the game
* hide Windows taskbar automatically whilst in game
* 1-4 players

### installation

install latest [Sandboxie](https://www.sandboxie.com/AllVersions). The official site is garbage, so you may use a mirror.

create 4 boxes in Sandboxies: `bo2_splitscreen_0`, `bo2_splitscreen_1`, `bo2_splitscreen_2`, `bo2_splitscreen_3`,  
configure in each one of them direct access to Steam install directory, Steam libraries and Borderlands 2 directory withing My Documents.

disable steam cloud sync for your Borderlands 2 saves  
(`Steam -> Library -> Borderlands 2 -> Properties .. -> Updates -> Steam Cloud -> Enable Steam Cloud sync for Borderlands 2`).  
This is necessary since you'll be running multiple instances from the single Steam user.  

```bash
pipenv install
```

this code doesn't care if you have localized game as long as the binary is the same (`Borderlands2.exe`)

### usage

run `bo2_splitscreen.py` with Python 3.8

### todos

* download and install sandboxie automatically
* autocreate sandboxie boxes if they're absent, autoconfigure their settings
* autodiscover sandboxie binary path
* autodiscover bo2 binary path
* autodiscover steam binary path
* launch steam automatically inside the each sandboxie box before launching the game.  
First one (server) should run Steam online, other offline.  
Steam instances must launch withing timeouts, otherwise there would be dll access issue
* freeze the app via py2exe / pyinstaller
* add simple GUI instead of / in addition to current CLI
* provide beautiful instructions
* provide gif / youtube demo how it works for end user
* cover with tests
* add static linting
