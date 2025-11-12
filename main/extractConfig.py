import zipfile
import logging
import os

logger = logging.getLogger("steamCrack")

def extractConfig(configPath):
    

    if not configPath:
        logger.error("No config path provided.")
        return

    if not os.path.exists(configPath):
        logger.error(f"File not found: {configPath}")
        return

    try:
        logger.info(f"Opening ZIP: {configPath}")
        with zipfile.ZipFile(configPath, 'r') as zipFile:
            logger.info("Contents of ZIP file:")
            zipFile.printdir()
            
            zipFile.extractall('./')
            logger.info(f"{configPath} extraction complete.")
            placeConfig()
            return 200

    except zipfile.BadZipFile:
        logger.error(f"{configPath} is not a valid ZIP file or is corrupted.")
    except Exception as e:
        logger.error(f"Something went wrong while extracting {configPath}: {e}")


def placeConfig():

    for file in os.listdir("."):
        if file.endswith(".lua"):
            print("This is lua file")
            print(file)
        elif file.endswith(".manifest"):
            print("This is manifest File")
            print (file)

        
