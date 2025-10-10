import zipfile
import logging


def extractConfig(configPath, configZip):

    logger = logging.getLogger("steamCrack")

    if configZip:

        logger.info(f"Game config path : {configPath} ...... ")
        with zipfile.ZipFile(configZip, 'r') as zipFile:
            zipFile.extractall('./')
            logger.info(f"{configZip} Extraction complete ......")

            return 200



    
    
    


