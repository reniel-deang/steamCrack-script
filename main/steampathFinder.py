import os
import winreg
import logging


def getsteamPath():
    logger = logging.getLogger("steamCrack")
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Valve\\Steam")
        steamPath, _ = winreg.QueryValueEx(key, "SteamPath")
        winreg.CloseKey(key)
        print(steamPath)

        return steamPath

    except FileNotFoundError as e :
        logger.error(f"Something went wrong in steampathFinder.py . read output : {e}")

if __name__ == "__main__":
    pass
    # steampath = getsteamPath()
    # fullpath = os.path.join(steampath, "config")
    # print(fullpath)
