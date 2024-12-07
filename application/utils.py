import requests
import logging

DATA_URL = "http://127.0.0.1:8000/Data"
INFERENCE_URL = "http://127.0.0.1:8000/inference/{user_id}"
UPDATE_URL = "http://127.0.0.1:8000/health_updates/{user_id}"
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
    response = requests.get(full_url, headers=HEADERS, params=params)

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

# print(inference("101664654052127013363854956795422032758", "Hi"))
# print("------------------------")
# print(update("101664654052127013363854956795422032758"))