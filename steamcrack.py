# ----- THIS WILL BE THE MAIN CODE TO RUN ------

import os
from main import tests3
from dotenv import load_dotenv


if __name__ == "__main__":

    load_dotenv()
    
    currentPath = os.path.dirname(os.path.abspath(__file__))
    configFolder="fetchDb"
    depotCache="depotcache"
    stPlugin="stplug-in"

    gamePath=os.path.join(currentPath, configFolder)


    if not os.path.isdir(gamePath):
        os.mkdir(gamePath)
        print(f"Making directory in \"{gamePath}\" Successfull ......")
    else:
        print(f"Path \"{gamePath}\" Already Existing ......")
    print(gamePath)
    
    depotCache=os.path.join(gamePath, "deptcache")
    stPlugin=os.path.join(gamePath, "stplug-in")

    if not os.path.isdir(depotCache) and not os.path.isdir(stPlugin):
        os.mkdir(depotCache)
        os.mkdir(stPlugin)
    else:
        print("Folder depot and stPlugin are already existing ......")

    # ---- Sample game to fetch ----
    tests3.fetchGame(1030300, os.getenv('STEAMCONFIG_HOST'))



