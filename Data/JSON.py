import json
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from project_utils import get_logger

logger = get_logger(__name__)

# Directory to store JSON files
USER_JSON_FOLDER = "./data"
if not os.path.exists(USER_JSON_FOLDER):
    os.makedirs(USER_JSON_FOLDER)

# Establishing MongoDB connection
def database_conn():
    connection_line = "mongodb+srv://ahmadbsds:0177756@cluster0.h62ah.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    logger.info("Connecting to database")
    my_client = MongoClient(connection_line)
    logger.info("Success client")

    # Confirm connection
    try:
        my_client.admin.command("ping")
        logger.info("Pinged your deployment. Successfully connected to MongoDB!")
    except Exception as e:
        logger.error(e)
    # Database and collection
    my_db = my_client["app"]  # 'app' is the database
    data_table = my_db["User"]  # 'User' is the collection
    return data_table

table_data = None
try:
    table_data = database_conn()
    logger.info("Database connection successful.")
except Exception as e:
    logger.error("Error establishing database connection.", e)


# Utility function to save data to JSON
def save_to_json(data, user_id):
    """Save user data to a unique JSON file."""
    file_path = os.path.join(USER_JSON_FOLDER, f"user_{user_id}.json")
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    logger.info(f"User data saved to JSON file: {file_path}")


# Function to add user data
def add_data(user_id, name, email, password, data_table=table_data):
    """Add new user data to MongoDB and export to JSON."""
    logger.info("Adding data to database")
    user_data = {
        "id": user_id,
        "name": name,
        "email": email,
        "password": password,
    }
    # Insert into MongoDB
    data_table.insert_one(user_data)
    logger.info("Success adding data to database")

    # Save to JSON
    save_to_json(user_data, user_id)


# Function to get user data by ID
def get_user_by_id(user_id, data_table=table_data):
    """Retrieve user data by ID and save to JSON."""
    myquery = {"id": user_id}
    logger.info("Getting user data from MongoDB.")
    mydata = data_table.find_one(myquery)  # Returns a single document
    if mydata:
        logger.info("Success getting user data from MongoDB.")
        save_to_json(mydata, user_id)  # Export to JSON
        return mydata
    else:
        logger.warning(f"No user found with ID: {user_id}")
        return None


# Function to get user data by email
def get_user_data_by_mail(email, data_table=table_data):
    """Retrieve user data by email and save to JSON."""
    myquery = {"email": email}
    logger.info("Getting user data from MongoDB.")
    mydata = data_table.find_one(myquery)  # Returns a single document
    if mydata:
        logger.info("Success getting user data from MongoDB.")
        save_to_json(mydata, mydata["id"])  # Export to JSON
        return mydata
    else:
        logger.warning(f"No user found with email: {email}")
        return None
