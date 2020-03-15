### purpose

run Borderlands 2 on PC with split screen for set number of players. Windows only.

### features

* support for multi-monitor configurations
* support for localized versions of the game
* Windows taskbar automatic hiding
* 1-4 players

### installation

install latest [Sandboxie](https://www.sandboxie.com/AllVersions). The official site is garbage, so you may use a mirror.

disable steam cloud sync for your Borderlands 2 saves
(Steam -> Library -> Borderlands 2 -> Properties .. -> Updates -> Steam Cloud -> Enable Steam Cloud sync for Borderlands 2).

This is necessary since you'll be running multiple instances from the single Steam user.

```bash
pipenv install
```

this code doesn't care if you have localized game as long as the binary is the same (`Borderlands2.exe`)

### usage

run `bo2_splitscreen.py` with Python 3.8

### todos

* run explorer again after all bo2 instances were terminated
* tweak height resolution if possible
* download and install sandboxie automatically
* autodiscover sandboxie binary path
* autodiscover bo2 binary path
* autodiscover steam binary path
* autocreate sandboxie boxes if they're absent, autoconfigure their settings
* launch steam automatically inside the each sandboxie box before launching the game.  
First one (server) should run Steam online, other offline
* freeze the app via py2exe / pyinstaller
* add simple GUI instead of / in addition to current CLI
* provide beautiful instructions
* provide gif / youtube demo how it works for end user
* cover with tests
* add static linting
