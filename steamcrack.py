# ----- THIS WILL BE THE MAIN CODE TO RUN ------

import os
from dotenv import load_dotenv
from main import steampathFinder, fetchConfig, checkDir, logger


if __name__ == "__main__":

    currentPath = os.path.dirname(os.path.abspath(__file__))
    steampath = steampathFinder.getsteamPath()
    configFolder = os.path.join(steampath, "config")

    # --- Get a logger for this module ---
    logger = logger.setupLogger("steamCrack")

    logger.info(" ---------- Starting steamCrack script ----------")

    # ---Note that you need here a .env file. If you need it, just message me
    load_dotenv()

    # --- Run checkDir.py ---
    checkDir.checkDir(configFolder)

    fetchConfig.fetchGame(2973500, configFolder, os.getenv('STEAMCONFIG_HOST'))


