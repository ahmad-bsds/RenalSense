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


def extract_text_from_uploaded_file(file):
    from io import BytesIO
    import os
    import docx2txt
    from PyPDF2 import PdfReader
    """
    Extract text from an uploaded file (Flask's FileStorage object).
    Supports .txt, .docx, and .pdf files.
    """
    filename = file.filename
    _, file_extension = os.path.splitext(filename)
    file_extension = file_extension.lower()

    if file_extension == '.txt':
        # Read text directly from the file stream
        file.stream.seek(0)
        return file.stream.read().decode('utf-8')
    elif file_extension == '.docx':
        # Process .docx file from in-memory bytes
        file.stream.seek(0)
        return docx2txt.process(BytesIO(file.read()))
    elif file_extension == '.pdf':
        # Process .pdf file from the file stream
        file.stream.seek(0)
        pdf_reader = PdfReader(file.stream)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


# print(inference("101664654052127013363854956795422032758", "Hi"))
# print("------------------------")
# print(update("101664654052127013363854956795422032758"))