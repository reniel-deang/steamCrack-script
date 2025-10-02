import requests

# The URL you provided, replace {appid} with your actual appid
appid = "1030300"  # Replace this with the actual appid you want to test
url = f"" # need env

# Path to save the downloaded file
file_path = f"./{appid}.zip"

try:
    # Sending a GET request to the URL
    response = requests.get(url)
    
    # Check if the response status is OK (200)
    if response.status_code == 200:
        # Open the file in write-binary mode and save the content
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully: {file_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        print(response.text)  # You can print the response body for debugging
    
except Exception as e:
    print(f"An error occurred: {e}")




# url = ""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    with open('file.zip', 'wb') as f:
        f.write(response.content)