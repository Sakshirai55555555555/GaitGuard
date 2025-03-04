import pandas as pd
import os
from flask import request
import time
from flask import Flask, render_template, request, jsonify, redirect, flash, send_from_directory
from werkzeug.utils import secure_filename
from config.config import LocalDevelopmentConfig
from Modelss.database import db
from Modelss.models import User
from utils.process_video import process_video
from utils.recommendations import recommend
from sqlalchemy import or_, and_
from flask import Flask, render_template, request, redirect, flash, url_for
from Modelss.database import db
from Modelss.models import User
from sqlalchemy import and_

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    
    # Set up folders for uploads and processed videos
    app.config['UPLOAD_FOLDER'] = "uploads"
    app.config['PROCESSED_FOLDER'] = "processed_videos"
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    @app.route("/", methods=["GET", "POST"])
    def index():
        processed_video_url = None
        if request.method == "POST":
            if "video" not in request.files:
                return jsonify({"error": "No file uploaded!"})

            file = request.files["video"]
            if file.filename == "":
                return jsonify({"error": "No selected file!"})

            if not allowed_file(file.filename):
                return jsonify({"error": "Invalid file type! Only MP4, AVI, MOV are allowed."})

            filename = secure_filename(file.filename)
            unique_filename = f"{filename.rsplit('.', 1)[0]}_{int(time.time())}.mp4"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
            file.save(filepath)

            result = process_video(filepath, app.config['PROCESSED_FOLDER'])
            processed_video_filename = result.get("processed_video", None)
            if processed_video_filename:
                processed_video_url = f"/processed_videos/{processed_video_filename}"

            final_prediction = result.get("final_prediction", "Unknown")
            recommendation_text = recommend(final_prediction)

            print("Processed video file path:", processed_video_url)  # Debug output

            response = {      
                "results": result,
                "recommendation": recommendation_text.replace("\n", "<br>"),
                "processed_video_url": processed_video_url
            }
            return jsonify(response)
        return render_template("index.html", processed_video_url=processed_video_url)
    
    @app.route('/processed_videos/<filename>')
    def processed_videos(filename):
        return send_from_directory('processed_videos', filename, mimetype='video/mp4')

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            security_question = request.form.get("security_question")
            security_answer = request.form.get("security_answer")

            if not (username and email and password and security_question and security_answer):
                flash("Please fill out all fields!")
                return redirect("/signup")

            new_user = User(
                username=username,
                email=email,
                password=password,
                security_question=security_question,
                security_answer=security_answer
            )
            db.session.add(new_user)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash("Username or Email already exists!")
                return redirect("/signup")

            flash("Signup successful! Please login.")
            return redirect("/login")
        return render_template("signup.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            identifier = request.form.get("username")
            password_val = request.form.get("password")
            user = User.query.filter(
                and_(
                    or_(User.username == identifier, User.email == identifier),
                    User.password == password_val
                )
            ).first()

            if user:
                flash("Logged in successfully!")
                return redirect("/")
            else:
                flash("Invalid credentials. Please try again.")
                return redirect("/login")
        return render_template("login.html")

    @app.route("/forgot_password", methods=["GET", "POST"])
    def forgot_password():
        if request.method == "POST":
            username = request.form.get("username")
            security_question = request.form.get("security_question")
            security_answer = request.form.get("security_answer")
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")

            if new_password != confirm_password:
                flash("Passwords do not match!", "danger")
                return redirect(url_for("forgot_password"))

            user = User.query.filter_by(
                username=username,
                security_question=security_question,
                security_answer=security_answer
            ).first()

            if user:
                user.password = new_password  # If using hashing, replace with hashed password
                db.session.commit()  # ✅ Ensure the change is saved
                flash("Password updated successfully! Please log in.", "success")
                return redirect(url_for("login"))
            else:
                flash("Invalid security details. Please try again.", "danger")
                return redirect(url_for("forgot_password"))

        return render_template("forgot_password.html")
    
    @app.route('/submit_review', methods=['POST'])

    def submit_review():
        data = request.get_json()
        name = data.get('name', 'Anonymous')
        stars = data.get('stars', 0)
        comment = data.get('comment', '')

        #       Prepare data to save
        review_data = {
            'Name': [name],
            'Stars': [stars],
            'Comment': [comment]
        }
        df = pd.DataFrame(review_data)

        # Define file path
        file_path = 'reviews.csv'

        # Save to CSV (append if exists, create new if not)
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', index=False, header=False)
        else:
             df.to_csv(file_path, mode='w', index=False)

        return {'status': 'success'}
    
    @app.route("/mainhome")
    def mainhome():
        return render_template("mainhome.html")
    

    @app.route("/test_users")
    def test_users():
        users = User.query.all()
        user_list = []
        for user in users:
            user_list.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "password": user.password,
                "security_question": user.security_question,
                "security_answer": user.security_answer
            })
        return jsonify(user_list)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
