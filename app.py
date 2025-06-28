from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import mysql.connector
from mysql.connector import Error
import pytz
from werkzeug.utils import secure_filename

# Initialize Flask app with static folder configuration
app = Flask(__name__, static_folder='static', static_url_path='/static')
# The secret key is required by Flask for:
# 1. Securely signing the session cookie
# 2. Using flash messages
# 3. CSRF protection in forms
# This should be a complex random string in production
app.config['SECRET_KEY'] = 'TravelHub_2025'  # Change this in production

# Configure upload folder for resort images
UPLOAD_FOLDER = os.path.join('static', 'pics')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Database credentials
DB_USER = 'root'  # Changed from 'root@%' to just 'root'
DB_PASSWORD = 'Woaixuexi123'
DB_NAME = 'travelhub_2025'

# Configure SQLAlchemy to use mysql-connector-python
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@127.0.0.1/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Get US Eastern timezone
eastern = pytz.timezone('US/Eastern')

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    """Save uploaded image to the pics directory"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to make it unique
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return filename
    return None

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(eastern))
    is_admin = db.Column(db.Boolean, default=False)
    age = db.Column(db.Integer)
    resorts = db.relationship('UserResort', backref='user', lazy=True)

class Resort(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    county = db.Column(db.String(100))
    pic_location = db.Column(db.String(200))
    user_resorts = db.relationship('UserResort', backref='resort', lazy=True)

class UserResort(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    resort_id = db.Column(db.Integer, db.ForeignKey('resort.id'), nullable=False)
    like = db.Column(db.Boolean)
    expense = db.Column(db.Numeric(10, 2))
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(eastern))
    recommendation = db.Column(db.Integer)

def create_database():
    try:
        # Connect to MySQL server as root
        connection = mysql.connector.connect(
            host="127.0.0.1",  # Changed from localhost to 127.0.0.1 to match SQLAlchemy URI
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            print("Connected to MySQL server")
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print(f"Database {DB_NAME} created successfully")
            
            # Switch to the new database
            cursor.execute(f"USE {DB_NAME}")
            
            # Create tables
            with app.app_context():
                db.create_all()
                print("Tables created successfully")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Routes
@app.route('/')
def home():
    resorts = Resort.query.all()
    # Prepare stats for each resort
    resort_stats = {}
    for resort in resorts:
        user_resorts = resort.user_resorts
        count = len(user_resorts)
        if count > 0:
            total_expense = sum([float(ur.expense) for ur in user_resorts if ur.expense is not None])
            total_recommendation = sum([int(ur.recommendation) for ur in user_resorts if ur.recommendation is not None])
            count_expense = len([ur for ur in user_resorts if ur.expense is not None])
            count_recommendation = len([ur for ur in user_resorts if ur.recommendation is not None])
            avg_expense = total_expense / count_expense if count_expense > 0 else None
            avg_recommendation = total_recommendation / count_recommendation if count_recommendation > 0 else None
        else:
            avg_expense = None
            avg_recommendation = None
        resort_stats[resort.id] = {
            'avg_expense': avg_expense,
            'avg_recommendation': avg_recommendation
        }
    return render_template('home.html', resorts=resorts, resort_stats=resort_stats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('signup'))
        
        new_user = User(username=username, password=password, age=age)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/add_resort', methods=['GET', 'POST'])
def add_resort():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Handle image upload
        image_file = request.files.get('resort_image')
        image_filename = save_image(image_file) if image_file else None
        
        # Create new resort
        new_resort = Resort(
            name=request.form['name'],
            country=request.form['country'],
            state=request.form['state'],
            city=request.form['city'],
            county=request.form['county'],
            type=request.form['resort_type'],
            pic_location=image_filename
        )
        
        db.session.add(new_resort)
        db.session.commit()
        
        # Create user resort relationship
        user_resort = UserResort(
            user_id=session['user_id'],
            resort_id=new_resort.id,
            expense=request.form['expense'],
            recommendation=request.form['recommendation'],
            comment=request.form['comment']
        )
        
        db.session.add(user_resort)
        db.session.commit()
        
        flash('Resort added successfully!')
        return redirect(url_for('profile'))
    
    return render_template('add_resort.html')

@app.route('/resort/<int:resort_id>')
def resort_detail(resort_id):
    resort = Resort.query.get_or_404(resort_id)
    
    # Calculate total likes and dislikes
    likes = UserResort.query.filter_by(resort_id=resort_id, like=True).count()
    dislikes = UserResort.query.filter_by(resort_id=resort_id, like=False).count()
    
    # Get user's vote if logged in
    user_vote = None
    if 'user_id' in session:
        user_resort = UserResort.query.filter_by(
            user_id=session['user_id'],
            resort_id=resort_id
        ).first()
        if user_resort:
            user_vote = 'up' if user_resort.like else 'down'
    
    return render_template('resort_detail.html', 
                         resort=resort, 
                         likes=likes, 
                         dislikes=dislikes,
                         user_vote=user_vote)

@app.route('/resort/<int:resort_id>/vote', methods=['POST'])
def vote_resort(resort_id):
    if 'user_id' not in session:
        flash('Please login to vote', 'warning')
        return redirect(url_for('login'))
    
    resort = Resort.query.get_or_404(resort_id)
    vote = request.form.get('vote')
    
    # Check if user already has a UserResort entry
    user_resort = UserResort.query.filter_by(
        user_id=session['user_id'],
        resort_id=resort_id
    ).first()
    
    if user_resort:
        # Update existing like status
        user_resort.like = (vote == 'up')
    else:
        # Create new UserResort entry
        user_resort = UserResort(
            user_id=session['user_id'],
            resort_id=resort_id,
            like=(vote == 'up')
        )
        db.session.add(user_resort)
    
    db.session.commit()
    flash('Vote recorded successfully', 'success')
    return redirect(url_for('resort_detail', resort_id=resort_id))

@app.route('/resort/<int:resort_id>/comment', methods=['POST'])
def add_comment(resort_id):
    if 'user_id' not in session:
        flash('Please login to comment', 'warning')
        return redirect(url_for('login'))
    
    content = request.form.get('comment')
    expense = request.form.get('expense')
    recommendation = request.form.get('recommendation')
    
    if not content:
        flash('Comment cannot be empty', 'warning')
        return redirect(url_for('resort_detail', resort_id=resort_id))
    
    # Check if user already has a UserResort entry
    user_resort = UserResort.query.filter_by(
        user_id=session['user_id'],
        resort_id=resort_id
    ).first()
    
    if user_resort:
        # Update existing entry
        user_resort.comment = content
        if expense:
            user_resort.expense = expense
        if recommendation:
            user_resort.recommendation = recommendation
    else:
        # Create new UserResort entry
        user_resort = UserResort(
            user_id=session['user_id'],
            resort_id=resort_id,
            comment=content,
            expense=expense if expense else None,
            recommendation=recommendation if recommendation else None
        )
        db.session.add(user_resort)
    
    db.session.commit()
    flash('Comment added successfully', 'success')
    return redirect(url_for('resort_detail', resort_id=resort_id))

if __name__ == '__main__':
    # Create database and tables before running the app
    create_database()
    app.run(debug=True) 