from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import os
from werkzeug.utils import secure_filename
from simple_predict import SimplePredictor
import pandas as pd
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Configure upload folders
UPLOAD_FOLDER = 'uploads'
PREDICTION_FOLDER = 'Prediction_Output_File'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PREDICTION_FOLDER):
    os.makedirs(PREDICTION_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
@cross_origin()
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
@cross_origin()
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # Hash the password
        hashed_password = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                     (username, hashed_password, email))
            conn.commit()
            conn.close()
            flash('Registration successful! Please login.')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists!')
            return redirect(url_for('register'))
        except Exception as e:
            flash(f'Error during registration: {str(e)}')
            return redirect(url_for('register'))
            
    return render_template('register.html')

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    username = request.form['username']
    password = request.form['password']
    
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):  # user[2] is the hashed password
            session['username'] = username
            session['user_id'] = user[0]  # Store user ID in session
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error during login: {str(e)}')
        return redirect(url_for('index'))

@app.route('/logout')
@cross_origin()
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@cross_origin()
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    # Initialize stats (replace with real data in production)
    stats = {
        'total_predictions': 0,
        'fraud_count': 0,
        'valid_count': 0
    }
    
    return render_template('results.html', 
                         total_predictions=stats['total_predictions'],
                         fraud_count=stats['fraud_count'],
                         valid_count=stats['valid_count'])

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():
    if 'username' not in session:
        return redirect(url_for('index'))
        
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('dashboard'))
        
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('dashboard'))
        
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Make predictions
            predictor = SimplePredictor()
            output_path = os.path.join(PREDICTION_FOLDER, 'Predictions.csv')
            predictor.predict(filepath, output_path)
            
            # Read predictions
            predictions_df = pd.read_csv(output_path)
            
            # Calculate stats
            total_predictions = len(predictions_df)
            fraud_count = (predictions_df['Predictions'] == 'Y').sum()
            valid_count = (predictions_df['Predictions'] == 'N').sum()
            
            # Format predictions for display
            predictions = []
            for idx, row in predictions_df.iterrows():
                predictions.append({
                    'id': idx + 1,
                    'status': row['Predictions'],
                    'confidence': 95  # Replace with actual confidence if available
                })
            
            return render_template('results.html',
                                total_predictions=total_predictions,
                                fraud_count=fraud_count,
                                valid_count=valid_count,
                                predictions=predictions)
                                
        except Exception as e:
            flash(f'Error during prediction: {str(e)}')
            return redirect(url_for('dashboard'))
            
    else:
        flash('Invalid file format. Please upload a CSV file.')
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(port=port, debug=True) 