import logging
import os
from pathlib import Path

def setupLogger(name: str = "steamCrack"):

    # -- Path of logs folder -- 
    # -- As long as it running on virtual environment, it always point on the root of ./steamCrack directory
    logDir = Path("logs")
    
    # if ./logs is not exist then make a directory
    if not logDir.is_dir():
        os.makedirs(logDir)
    
    # logfile filepath
    logFile = os.path.join(logDir, "logs.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # # Always reset handlers so logging works on every run
    # logger.handlers.clear()

    if not logger.handlers:
        formatter = logging.Formatter(
            "{asctime} - {levelname} - {name} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%m:%S"
        )
        
        fileHandler = logging.FileHandler(logFile, mode="a", encoding="utf-8")
        fileHandler.setFormatter(formatter)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)
        logger.addHandler(consoleHandler)

        return logger
        

# def startLog():
#     logDir=f"./logs"
#     if not os.path.isdir(logDir):
#        os.makedirs(logDir)
        
    
#     log_file = os.path.join(logDir, "script.log")
#     logging.basicConfig(
#         style="{",
#         format="{asctime} - {levelname} - {message}",
#         datefmt="%Y-%m-%d %H:%M:%S",
#         handlers=
#         [
#             logging.FileHandler(log_file),
#             logging.StreamHandler()
#         ]
#     )

#     return logging.info("Module logger.py success .....")
