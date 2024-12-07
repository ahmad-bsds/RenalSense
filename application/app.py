from flask import Flask, render_template, request, redirect, flash, jsonify, url_for
from .utils import get_logger
from infrastructure.utils import RegistrationForm, LoginForm
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from infrastructure.utils import hashPass, matchHash
import uuid
import json
import os
from werkzeug.utils import secure_filename
import docx2txt
import PyPDF2
from application.utils import data_send, update, inference


logger = get_logger(__name__)

# Flask setup.
flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = '$Renal-Sense$'
idd = uuid.uuid1().int.__str__()  # for generating random ids.
login_manager = LoginManager()
login_manager.init_app(flask_app)

# ================== User dashboard management ====================
# Sample Data
#
# recommendations = [
#     {
#         'stage': 3,
#         'risk': "High"
#     },
#     {'icon': 'fas fa-utensils', 'title': 'Low-sodium diet',
#      'description': 'Aim for less than 2,000mg of sodium per day'},
#     {'icon': 'fas fa-glass-water', 'title': 'Stay hydrated', 'description': 'Drink 8-10 glasses of water daily'},
#     {'icon': 'fas fa-dumbbell', 'title': 'Regular exercise',
#      'description': '30 minutes of moderate activity, 5 days a week'}
# ]
#
# health_stats = recommendations[0]




# Chatbot response
BOT_RESPONSE = "Welcome!"

# File upload variables
uploaded_file = None
file_flag = None


# User dashboard where insights will be shown.
@flask_app.route('/user_home')
@login_required
def user_home():
    # # Get the Data.
    logger.info(f"User {current_user.id} is getting in........")
    # try:
    #     data = update(str(current_user.id))
    #     logger.info("Data fetched!")
    # except Exception as e:
    #     logger.error("Recommendation and updates failed!", e)

    data = {'stage': 0, 'risk': 'Error', 'recommendations': ['Maintain a healthy diet', 'Stay hydrated', 'Exercise regularly', 'Get regular check-ups']}
    # Check if 'recommendations' is not a list
    if not isinstance(data['recommendations'], list):
        # Convert it to a list
        data['recommendations'] = [data['recommendations']]
    return render_template('user_home.html', health_stats= {'stage': data['stage'], 'risk': data['risk']}, recommendations= data['recommendations'])
   # return render_template('user_home.html', health_stats=health_stats, recommendations=recommendations)

# settings page
@flask_app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


# On refresh.
@flask_app.route('/refresh', methods=['POST'])
@login_required
def refresh():
    # return redirect(url_for('user_home.html'))
    pass

# User chat
@flask_app.route('/chat', methods=['POST'])
@login_required
def chat():
    user_message = request.form.get('message')
    print(f"User: {user_message}")
    return jsonify({'response': inference(user_id=str(current_user.id), prompt=user_message)})


# when user upload something.

@flask_app.route('/upload', methods=['POST'])
@login_required
def upload():
    global uploaded_file, file_flag
    file = request.files['file']
    if file:
        filename = file.filename
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in ['.jpg', '.jpeg', '.png']:
            file_flag = 0
        elif file_ext in ['.txt']:
            file_flag = 1
        else:
            return jsonify({'status': 'error', 'message': 'Unsupported file type'})

        uploaded_file = file
        return jsonify({'status': 'success', 'filename': filename})
    return jsonify({'status': 'error', 'message': 'No file uploaded'})


# ========================== User settings management =================

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx', 'pdf'}

flask_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    elif file_extension == '.docx':
        return docx2txt.process(file_path)
    elif file_extension == '.pdf':
        pdf_reader = PyPDF2.PdfFileReader(file_path)
        text = ''
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
        return text
    else:
        return None


@flask_app.route('/submit', methods=['POST'])
def submit():
    age = request.form.get('age')
    gender = request.form.get('gender')
    height = request.form.get('height')
    fatigue = request.form.get('fatigue')
    concentration = request.form.get('concentration')
    sleep = request.form.get('sleep')
    appetite = request.form.get('appetite')
    cramping = request.form.get('cramping')
    swollen_feet = request.form.get('swollen_feet')
    puffiness = request.form.get('puffiness')
    dry_skin = request.form.get('dry_skin')
    urination = request.form.get('urination')
    nausea = request.form.get('nausea')
    vomiting = request.form.get('vomiting')
    urine_output = request.form.get('urine_output')
    pericardium = request.form.get('pericardium')
    blood_pressure = request.form.get('blood_pressure')
    comment = request.form.get('comment')
    files = request.files.getlist('file-upload')

    # Process the Data as needed
    response = {

        "Age": age,
        "Gender": gender,
        "Height": height,
        "Fatigue": fatigue,
        "Concentration": concentration,
        "Sleep": sleep,
        "Appetite": appetite,
        "Cramping": cramping,
        "Swollen Feet": swollen_feet,
        "Puffiness": puffiness,
        "Dry Skin": dry_skin,
        "Urination": urination,
        "Nausea": nausea,
        "Vomiting": vomiting,
        "Urine Output": urine_output,
        "Pericardium": pericardium,
        "Blood Pressure": blood_pressure,
        "Comment": comment,
        "Extracted Texts": []
    }

    # Save uploaded files and extract text
    extracted_texts = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(flask_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            logger.info(f"File saved: {filename}")

            # Extract text from the file
            text = extract_text_from_file(file_path)
            if text:
                extracted_texts.append(text)

    # Add extracted texts to the response
    response["Extracted Texts"] = extracted_texts

    try:
        data = {key: f"{value}" for key, value in response.items()}
        print("Data submitting...........................", data)
    except Exception as e:
        data = response
        logger.error(f"TypeError, adding data: {e}")

    # Add submitted Data.
    try:
        data_send(user_id=str(current_user.id), data=data)
        logger.info(f"Data added by {current_user.id}")
    except Exception as e:
        logger.error(f"Error adding data: {e}")


    # Redirect to a success page or perform other actions
    return redirect("user_home")

# ========================= User Management ==========================
# Signup.
@flask_app.route('/signUp', methods=['POST', 'GET'])
def signup():
    from infrastructure.mongo_db import add_data, chk_pass
    form = RegistrationForm()
    if request.method == 'POST':
        user_id = idd  # random id to store corresponding to a user who registered.
        # signup form credentials.
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        if not chk_pass(email):
            hashed = hashPass(password)
            add_data(user_id=user_id, name=name, email=email, password=str(hashed))
            logger.info(f"user {user_id} signed up.")
            return redirect('/app/settings')
        else:
            flash('Email already exists.')  # To show message.
    return render_template('signUp.html', form=form)


@flask_app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@login_manager.user_loader
def load_user(user_id):
    from infrastructure.utils import User
    return User.get(user_id)


@flask_app.route('/login', methods=['POST', 'GET'])
def login():
    from infrastructure.utils import User
    from infrastructure.mongo_db import chk_pass, get_user_data_by_mail
    """Login of user."""
    HASHPASS = ''
    form = LoginForm()  # object of form for login.
    if request.method == 'POST':  # if we are sending Data to server e.g filling fields.
        # get Data we entered in the fields
        email = request.form.get('email')
        password = request.form.get('password')
        if not chk_pass(email):  # if mail doesnt exists in database.
            flash('Email not found.')
        else:
            HASHPASS = chk_pass(email)  # if mail exists pass will be returned.
        if matchHash(HASHPASS, password):  # match hashed (hash_pass) and user entered pass.
            # For storing session of user who logged in.
            user_data = get_user_data_by_mail(email=email)
            # storing Data in blueprint of logged_user.
            user = User(user_data['id'], user_data['name'], user_data['email'], user_data['password'])
            # flask_login method to store session of logging.
            login_user(user)

            return redirect('/app/user_home')
        else:
            flash('Password error')
    return render_template('login.html', form=form)


@flask_app.route('/')
def home():
    return render_template('homepage.html')


if __name__ == "__main__":
    flask_app.run(debug=True)
