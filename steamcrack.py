# ----- THIS WILL BE THE MAIN CODE TO RUN ------

import os
from dotenv import load_dotenv
from main import fetchConfig, checkDir, logger


if __name__ == "__main__":

    currentPath = os.path.dirname(os.path.abspath(__file__))
    configFolder = "fetchDb"
    gamePath = os.path.join(currentPath, configFolder)

    # --- Get a logger for this module ---
    logger = logger.setupLogger("steamCrack")

    logger.info(" ---------- Starting steamCrack script ----------")

    # ---Note that you need here a .env file. If you need it, just message me
    load_dotenv()

    

    # --- Run checkDir.py ---
    checkDir.checkDir(gamePath)

    fetchConfig.fetchGame(2897760, configFolder, os.getenv('STEAMCONFIG_HOST'))


