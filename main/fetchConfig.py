import requests
import os
import logging
import pathlib as Path
from main import extractConfig

def fetchGame(gameID, configFolder, envLink):
    
    logger = logging.getLogger("steamCrack")

    if gameID:

        gameFile=f"{envLink}/{gameID}.zip"
        file_path = os.path.join(configFolder, f"{gameID}.zip")
        logger.info(f"Fetching with ID of {gameID} ...... ")

        try:

            response = requests.get(gameFile)
            if response.status_code == 200:
                logger.info(f"Your game ID Has found and has status code of 200 (OK) ......")
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                    logger.info(f"File {gameID}.zip downloaded ...... ")
                    checkExtract = extractConfig.extractConfig(file_path)#file_path

                    if checkExtract == 200:
                        logger.info(f"Extraction success ...... ")




            
            else:
                logger.error(f"Your game ID doesn't exist in our database ......")

        except Exception as e:
            logger.error(f"Something went wrong . read output : {e}")
    
    return logger.info("Module fetchConfig.py success ......")



# # Path to save the downloaded file
# file_path = f"./{appid}.zip"

# try:
#     # Sending a GET request to the URL
#     response = requests.get(url)
    
#     # Check if the response status is OK (200)
#     if response.status_code == 200:
#         # Open the file in write-binary mode and save the content
#         with open(file_path, 'wb') as file:
#             file.write(response.content)
#         print(f"File downloaded successfully: {file_path}")
#     else:
#         print(f"Failed to download the file. Status code: {response.status_code}")
#         print(response.text)  # You can print the response body for debugging
    
# except Exception as e:
#     print(f"An error occurred: {e}")




# # url = ""
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# response = requests.get(url, headers=headers)
# if response.status_code == 200:
#     with open('file.zip', 'wb') as f:
#         f.write(response.content)