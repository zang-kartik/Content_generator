import requests
import os

def getFile(modalId, s3Path):
    """
    Fetches and Store file using s2Path

    Parameters:
    - modalId (str) : Used to name file
    - s3Path  (str) : Path to fetch file from
    
    Returns:
    - string
    """
    store_path = "/home/ubuntu/package-chatbot/Data"
    file_path = os.path.join(store_path,modalId) #Path to store file temporarily

    try:
        response = requests.get(s3Path)
        if response.status_code == 200:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response.text)
        
        else:
            return False
        
    except Exception as e:
        return str(e)
    

    return "success"
    
    
