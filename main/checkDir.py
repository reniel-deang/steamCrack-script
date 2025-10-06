# --- CODE FOR CHECKING DIRECTORY IF EXISTING ---

import os
import logging

def checkDir(gameDir):
    
    # --- get logger configuration named 
    logger = logging.getLogger("steamCrack")

    if not os.path.isdir(gameDir):
        os.mkdir(gameDir)
        logger.info(f"Making directory in \"{gameDir}\" Successfull ......")
    else:
        logger.info(f"Path \"{gameDir}\" Already Existing ......")
    
    depotCache=os.path.join(gameDir, "depotcache")
    stPlugin=os.path.join(gameDir, "stplug-in")

    if not os.path.isdir(depotCache) and not os.path.isdir(stPlugin):
        os.mkdir(depotCache)
        os.mkdir(stPlugin)
        logger.info(f"Making depotcache and stplug-in folder in \"{gameDir}\" Successfull ......")
    else:

        logger.info(f"Folder depotcache and stplug-in in \"{gameDir}\" already existing ......")

    return logger.info("Module checkDir.py success ......")