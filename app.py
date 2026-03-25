from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'learnhub_secret_key_2024'

DB_PATH = os.path.join(os.path.dirname(__file__), 'learnhub.db')

# ─── Database Setup ────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            enrolled_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# ─── Static Course Data ─────────────────────────────────────────────────────────

COURSES = [
    {
        'id': 1,
        'title': 'Python for Beginners',
        'category': 'Programming',
        'instructor': 'Dr. Ananya Sharma',
        'duration': '6 weeks',
        'level': 'Beginner',
        'students': 4821,
        'rating': 4.8,
        'price': 'Free',
        'icon': 'bi-code-slash',
        'color': '#3B82F6',
        'description': 'Master Python fundamentals with hands-on projects. Covers variables, loops, functions, OOP, and file handling.',
        'topics': ['Variables & Data Types', 'Control Flow', 'Functions', 'OOP Basics', 'File I/O']
    },
    {
        'id': 2,
        'title': 'Web Development Bootcamp',
        'category': 'Web Dev',
        'instructor': 'Rahul Verma',
        'duration': '10 weeks',
        'level': 'Intermediate',
        'students': 3210,
        'rating': 4.7,
        'price': '₹999',
        'icon': 'bi-globe',
        'color': '#10B981',
        'description': 'Full-stack web development using HTML, CSS, JavaScript, Bootstrap, and Flask from scratch.',
        'topics': ['HTML5 & CSS3', 'JavaScript ES6+', 'Bootstrap 5', 'Flask Backend', 'SQLite DB']
    },
    {
        'id': 3,
        'title': 'Data Science with Pandas',
        'category': 'Data Science',
        'instructor': 'Prof. Meera Nair',
        'duration': '8 weeks',
        'level': 'Intermediate',
        'students': 2890,
        'rating': 4.9,
        'price': '₹1499',
        'icon': 'bi-bar-chart-fill',
        'color': '#8B5CF6',
        'description': 'Explore data analysis, visualization, and machine learning basics using Python, Pandas, and Matplotlib.',
        'topics': ['Pandas DataFrames', 'Data Cleaning', 'Matplotlib', 'NumPy', 'ML Intro']
    },
    {
        'id': 4,
        'title': 'UI/UX Design Fundamentals',
        'category': 'Design',
        'instructor': 'Sneha Kulkarni',
        'duration': '5 weeks',
        'level': 'Beginner',
        'students': 1750,
        'rating': 4.6,
        'price': 'Free',
        'icon': 'bi-palette-fill',
        'color': '#F59E0B',
        'description': 'Learn design thinking, wireframing, prototyping, and user research using Figma and design principles.',
        'topics': ['Design Thinking', 'Wireframing', 'Figma Basics', 'Color Theory', 'Prototyping']
    },
    {
        'id': 5,
        'title': 'Machine Learning A–Z',
        'category': 'AI/ML',
        'instructor': 'Dr. Kiran Reddy',
        'duration': '12 weeks',
        'level': 'Advanced',
        'students': 5120,
        'rating': 4.9,
        'price': '₹2499',
        'icon': 'bi-cpu-fill',
        'color': '#EF4444',
        'description': 'Comprehensive ML course covering supervised, unsupervised learning, neural networks, and deployment.',
        'topics': ['Linear Regression', 'Classification', 'Clustering', 'Neural Networks', 'Model Deployment']
    },
    {
        'id': 6,
        'title': 'Cloud Computing Basics',
        'category': 'Cloud',
        'instructor': 'Arun Menon',
        'duration': '7 weeks',
        'level': 'Beginner',
        'students': 2100,
        'rating': 4.5,
        'price': '₹799',
        'icon': 'bi-cloud-fill',
        'color': '#06B6D4',
        'description': 'Get started with cloud platforms — AWS, Azure, and GCP — and deploy real applications.',
        'topics': ['Cloud Concepts', 'AWS Basics', 'Storage & Compute', 'Serverless', 'DevOps Intro']
    }
]

# ─── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html', courses=COURSES)


@app.route('/courses')
def courses():
    category = request.args.get('category', 'All')
    search = request.args.get('search', '').strip().lower()
    filtered = COURSES
    if category != 'All':
        filtered = [c for c in filtered if c['category'] == category]
    if search:
        filtered = [c for c in filtered if search in c['title'].lower() or search in c['description'].lower()]
    categories = ['All'] + list({c['category'] for c in COURSES})
    return render_template('courses.html', courses=filtered, categories=categories, selected=category, search=search)


@app.route('/course/<int:course_id>')
def course_detail(course_id):
    course = next((c for c in COURSES if c['id'] == course_id), None)
    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('courses'))
    enrolled = False
    if 'user_id' in session:
        conn = get_db()
        row = conn.execute(
            'SELECT id FROM enrollments WHERE user_id=? AND course_id=?',
            (session['user_id'], course_id)
        ).fetchone()
        conn.close()
        enrolled = row is not None
    return render_template('course_detail.html', course=course, enrolled=enrolled)


@app.route('/enroll/<int:course_id>', methods=['POST'])
def enroll(course_id):
    if 'user_id' not in session:
        flash('Please log in to enroll in a course.', 'warning')
        return redirect(url_for('login'))
    course = next((c for c in COURSES if c['id'] == course_id), None)
    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('courses'))
    conn = get_db()
    existing = conn.execute(
        'SELECT id FROM enrollments WHERE user_id=? AND course_id=?',
        (session['user_id'], course_id)
    ).fetchone()
    if existing:
        flash(f'You are already enrolled in "{course["title"]}".', 'info')
    else:
        conn.execute(
            'INSERT INTO enrollments (user_id, course_id, enrolled_at) VALUES (?, ?, ?)',
            (session['user_id'], course_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        conn.commit()
        session['enrolled_course'] = course['title']
        conn.close()
        return redirect(url_for('success'))
    conn.close()
    return redirect(url_for('course_detail', course_id=course_id))


@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    course_title = session.pop('enrolled_course', 'the course')
    return render_template('success.html', course_title=course_title, user_name=session.get('user_name'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm = request.form.get('confirm_password', '').strip()

        errors = []
        if not name:
            errors.append('Full name is required.')
        if not email or '@' not in email:
            errors.append('A valid email address is required.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if password != confirm:
            errors.append('Passwords do not match.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('register.html', name=name, email=email)

        conn = get_db()
        existing = conn.execute('SELECT id FROM users WHERE email=?', (email,)).fetchone()
        if existing:
            flash('An account with this email already exists.', 'danger')
            conn.close()
            return render_template('register.html', name=name, email=email)

        conn.execute(
            'INSERT INTO users (name, email, password, created_at) VALUES (?, ?, ?, ?)',
            (name, email, password, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        conn.commit()
        conn.close()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return render_template('login.html', email=email)

        conn = get_db()
        user = conn.execute(
            'SELECT * FROM users WHERE email=? AND password=?', (email, password)
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return render_template('login.html', email=email)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to view your dashboard.', 'warning')
        return redirect(url_for('login'))
    conn = get_db()
    rows = conn.execute(
        'SELECT course_id, enrolled_at FROM enrollments WHERE user_id=? ORDER BY enrolled_at DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    enrolled_ids = {r['course_id']: r['enrolled_at'] for r in rows}
    my_courses = []
    for c in COURSES:
        if c['id'] in enrolled_ids:
            entry = dict(c)
            entry['enrolled_at'] = enrolled_ids[c['id']]
            my_courses.append(entry)
    return render_template('dashboard.html', my_courses=my_courses, user_name=session['user_name'])


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        errors = []
        if not name:
            errors.append('Name is required.')
        if not email or '@' not in email:
            errors.append('A valid email is required.')
        if not subject:
            errors.append('Subject is required.')
        if not message or len(message) < 10:
            errors.append('Message must be at least 10 characters.')
        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('contact.html', name=name, email=email, subject=subject, message=message)
        flash('Your message has been sent! We\'ll get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
