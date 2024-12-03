import pymongo.errors
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from project_utils import get_logger

logger = get_logger(__name__)


#Establishing mongo conn.
def database_conn():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    connection_line = "mongodb+srv://ahmadbsds:0177756@cluster0.h62ah.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Create a new client and connect to the server
    logger.info("Connecting to database")
    my_client = MongoClient(connection_line)
    logger.info("Success client")

    # Send a ping to confirm a successful connection
    try:
        my_client.admin.command('ping')
        logger.info("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        logger.error(e, my_client)
    # database
    my_db = my_client['app']  # app is my already created database.
    logger.info("Success app")
    # User is like a table in database app. For more see mongodb.
    data_table = my_db['User']
    logger.info("Success usr")
    return data_table


table_data = database_conn()


def add_data(user_id, name, email, password, data_table=table_data):
    """Used to add data user that will newly be added."""
    user_data = {
        "id": user_id,
        "name": name,
        "email": email,
        "password": password
    }
    return data_table.insert_one(user_data)


def chk_pass(email, data_table=table_data):
    """Function to match email in database and if matched then return password accordingly."""
    myquery = {"email": email}
    mydata = data_table.find(myquery)  # data type is mongodb cursor.
    for attributes in mydata:
        if email == attributes['email']:
            return attributes['password']
        else:
            return False


def get_user_by_id(user_id, data_table=table_data):
    """Get user data by id. Used in logedUser blueprint for getting user data by id. Essential for user_loader
    function."""
    myquery = {"id": user_id}
    mydata = data_table.find(myquery)  # data type is mongodb cursor.
    for attributes in mydata:
        return attributes


def get_user_data_by_mail(email, data_table=table_data):
    """Get user dta by email. Used in login function in app.py for getting data of login user by email and store
    session data."""
    myquery = {"email": email}
    mydata = data_table.find(myquery)  # data type is mongodb cursor.
    for attributes in mydata:
        return attributes

