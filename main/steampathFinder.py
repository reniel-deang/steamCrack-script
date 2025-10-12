import os
import winreg
import logging


def getsteamPath():
    logger = logging.getLogger("steamCrack")
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Valve\\Steam")

    except FileNotFoundError as e :
        logger.error(f"Something went wrong in steampathFinder.py . read output : {e}")
