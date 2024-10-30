# Import necessary modules from Flask
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session  # Import session handling from Flask-Session

# Initialize Flask application
app = Flask(__name__)

# Set a secret key for session management (replace 'your_secret_key' with a strong key in production)
app.secret_key = 'your_secret_key'  

# Configure session storage type (using the filesystem to store session data)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)  # Bind session to app for handling user sessions

# Simulated user database to store user data temporarily (in memory)
users = {}

# Define route for the home page
@app.route('/')
def index():
    # Retrieve logged-in user's username and email from the session
    username = session.get('username')
    email = session.get('email')
    # Render the index1.html template with username and email
    return render_template('index1.html', username=username, email=email)

# Define route for the signup functionality
@app.route('/signup', methods=['POST'])
def signup():
    # Retrieve form data from signup form
    username = request.form['username']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    
    # Check if the email already exists in the user database
    if email in users:
        # If email exists, display an error message and redirect to home
        flash('Email already exists. Please login.', 'danger')
        return redirect(url_for('index'))
    
    # Add new user to the simulated user database
    users[email] = {
        'username': username,
        'email': email,
        'phone': phone,
        'password': password
    }
    
    # Store username and email in session for user persistence
    session['username'] = username
    session['email'] = email
    # Display a success message and redirect to home
    flash(f'Signup successful! Welcome, {username}', 'success')
    return redirect(url_for('index'))

# Define route for the login functionality
@app.route('/login', methods=['POST'])
def login():
    # Retrieve form data from login form
    email = request.form['email']
    password = request.form['password']
    
    # Fetch the user record by email from the database
    user = users.get(email)
    # Check if user exists and the password matches
    if user and user['password'] == password:
        # If valid, store username and email in session
        session['username'] = user['username']
        session['email'] = email
        # Display a success message and redirect to home
        flash(f'Login successful! Welcome back, {user["username"]}', 'success')
        return redirect(url_for('index'))
    else:
        # If credentials are invalid, show an error and redirect to home
        flash('Invalid email or password.', 'danger')
        return redirect(url_for('index'))

# Define route for logging out the user
@app.route('/logout')
def logout():
    # Clear session data to log out the user
    session.clear()
    # Display a success message and redirect to home
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# Run the Flask application in debug mode for development
if __name__ == '__main__':
    app.run(debug=True)
