
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your-secret-key-replace-this'  # In production, use a secure secret key
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple user store - in production use a database
class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

users = {}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/')
def home():
    return render_template('index.html')

# Funnel Routes
@app.route('/squeeze')
def squeeze():
    return render_template('squeeze.html')

@app.route('/sales')
def sales():
    return render_template('sales.html')

@app.route('/oto1')
def oto1():
    return render_template('oto1.html')

@app.route('/oto2')
def oto2():
    return render_template('oto2.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/thank-you', methods=['GET', 'POST'])
def thank_you():
    if request.method == 'POST':
        # Here you would process the order
        # For now, just render the thank you page
        pass
    return render_template('thank-you.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    # Here you would typically save the email to a database
    # For now, we'll just return a success message
    return {'success': True, 'message': 'Thank you for signing up!'}

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/auth-callback')
def auth_callback():
    user_id = request.headers.get('X-Replit-User-Id')
    username = request.headers.get('X-Replit-User-Name')
    
    if user_id and username:
        user = User(user_id, username)
        users[user_id] = user
        login_user(user)
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
