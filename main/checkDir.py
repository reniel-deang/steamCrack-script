# --- CODE FOR CHECKING DIRECTORY IF EXISTING ---

import os
import logging

def checkDir(configFolder):
    
    # --- get logger configuration named 
    logger = logging.getLogger("steamCrack")

    if os.path.isdir(configFolder):
        depotCache=os.path.join(configFolder, "depotcache")
        stPlugin=os.path.join(configFolder, "stplug-in")

        try:
            if os.path.isdir(depotCache) and os.path.isdir(stPlugin):
                logger.info(f"Both depotcache and stplugin folder in directory {configFolder} exist ......")
            
            elif not os.path.isdir(depotCache) and os.path.isdir(stPlugin):
                logger.warning(f"depotcache folder not exist {configFolder} ......")
                logger.info(f"Making depotcache folder in {configFolder} ......")
                os.mkdir(depotCache)
                logger.info(f"Making directory sucessfull ......")

            elif os.path.isdir(depotCache) and not os.path.isdir(stPlugin):
                logger.warning(f"stplug-in folder not exist {configFolder} ......")
                logger.info(f"Making stplug-in folder in {configFolder} ......")
                os.mkdir(stPlugin)
                logger.info(f"Making directory sucessfull ......")
            
            else:
                logger.warning(f"No depotcache and stplug-in folder exist in {configFolder} ......")
                logger.info(f"Making both folder in {configFolder} ......")
                os.mkdir(depotCache)
                os.mkdir(stPlugin)
                logger.info(f"Making directory sucessfull ......")

        except Exception as e:
            logger.error(f"Something went wrong . read output : {e}")
            

    return logger.info("Module checkDir.py success ......")
            

        

    