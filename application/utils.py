import requests
import logging
from project_utils import get_logger, load_env_variable
import os
import shutil
logger = get_logger(__name__)

DATA_URL = "https://renalsense.onrender.com/Data"
INFERENCE_URL = "https://renalsense.onrender.com/inference/{user_id}"
UPDATE_URL = "https://renalsense.onrender.com/health_updates/{user_id}"
PASSWORD = load_env_variable("PASSWORD", "../.env")
EMAIL = load_env_variable("EMAIL", "../.env")

# Set the headers including the API key
HEADERS = {
    "Content-Type": "application/json",
    "access_token": "123"
}


def data_send(user_id: str, data: dict):
    # Define the Data to be sent
    data_item = {
        "id": user_id,
        "data": data
    }

    print(data_item)

    # Send the POST request
    response = requests.post(DATA_URL, json=data_item, headers=HEADERS)

    # Check the response
    if response.status_code == 200:
        print("Data sent successfully!")
        return response.json()
    else:
        print("Failed to send Data.")
        print("Status code:", response.status_code)
        print("Response:", response.text)



def inference(user_id: str, prompt: str):
    # Construct the full URL with the user_id
    full_url = INFERENCE_URL.format(user_id=user_id)

    # Set the query parameters
    params = {
        "prompt": prompt
    }

    # Send the GET request
    try:
        response = requests.get(full_url, headers=HEADERS, params=params)
        logger.info("Inference retrieved successfully! Ready to dispacth to front end.")
    except Exception as e:
        raise logger.error("Inference failed!", e)

    # Check the response
    if response.status_code == 200:
        print("Inference retrieved successfully!")
        return response.json()
    else:
        print("Failed to retrieve inference.")
        print("Status code:", response.status_code)
        print("Response:", response.text)



def update(user_id: str):
    # Construct the full URL with the user ID
    full_url = UPDATE_URL.replace("{user_id}", user_id)

    # Send the POST request
    response = requests.post(full_url, headers=HEADERS)

    # Check the response
    if response.status_code == 200:
        print("Health update sent successfully!")
        return response.json()
    else:
        print("Failed to send health update.")
        print("Status code:", response.status_code)
        print("Response:", response.text)

def get_logger(name: str) -> logging.Logger:
    """
    Template for getting a logger.

    Args:
        name: Name of the logger.

    Returns: Logger.
    """

    # Configure
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(name)

    return logger


def send_mail(name, personal_email, message, receiver):
    subject = f"Detailed report from RanelSense about {name}, email: {personal_email}"
    import smtplib
    # Establishing a connection.
    with smtplib.SMTP('smtp.gmail.com') as connection:
        # Security layer.
        connection.starttls()
        # Logining to email.
        connection.login(user=EMAIL, password=PASSWORD)
        # Sending mail.
        connection.sendmail(
            from_addr=EMAIL,  # address from send.
            to_addrs=receiver,  # address where send.
            msg=f"""Subject: {subject}\n\n 
            {message}.
            """
        )


import os

UPLOAD_FOLDER = './static/uploads'

def clear_upload_folder(folder_path):
    """
    Removes all files inside the specified folder.

    Args:
        folder_path (str): Path to the folder to clear.
    """
    try:
        # Ensure the folder exists
        if not os.path.exists(folder_path):
            print(f"The folder {folder_path} does not exist.")
            return

        # Iterate over all files in the folder and remove them
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Check if it's a file before removing
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Removed file: {file_path}")
            else:
                print(f"Skipped: {file_path} is not a file.")
        print("All files have been removed.")
    except Exception as e:
        print(f"An error occurred: {e}")


# print(inference("101664654052127013363854956795422032758", "Hi"))
# print("------------------------")
# print(update("101664654052127013363854956795422032758"))