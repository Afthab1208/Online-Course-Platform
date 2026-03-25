# 🎓 LearnHub — Online Course Learning Platform

A full-stack web application built with **Flask**, **Bootstrap 5**, **jQuery**, and **SQLite** that allows users to browse courses, register, log in, and enroll in online courses.

---

## 📸 Features

- 🏠 **Home Page** — Hero section, featured courses, testimonials, CTA
- 📚 **Courses Page** — Browse, search, and filter by category
- 🔍 **Course Detail** — Full info, topics, instructor, enrollment button
- ✅ **Enrollment Flow** — Confirmation modal → success page
- 👤 **User Auth** — Register & Login with form validation
- 📊 **Dashboard** — Track enrolled courses per user
- 📬 **Contact Form** — Validated contact page
- 🗄️ **SQLite Database** — Stores users and enrollments

---

## 🛠️ Technologies Used

| Layer       | Technology                    |
|-------------|-------------------------------|
| Frontend    | HTML5, Bootstrap 5, CSS3      |
| Scripting   | JavaScript, jQuery 3.7        |
| Backend     | Python 3, Flask 3             |
| Templating  | Jinja2                        |
| Database    | SQLite (via Python sqlite3)   |
| Icons       | Bootstrap Icons               |
| Fonts       | Google Fonts (Syne, DM Sans)  |

---

## 📁 Project Structure

```
online_course_platform/
├── app.py                  # Flask application (routes, DB logic)
├── learnhub.db             # SQLite database (auto-created)
├── requirements.txt        # Python dependencies
├── README.md
├── static/
│   ├── css/
│   │   └── style.css       # Custom styles
│   └── js/
│       └── main.js         # jQuery interactions
└── templates/
    ├── base.html           # Base layout (navbar, footer)
    ├── index.html          # Home page
    ├── courses.html        # All courses with filter
    ├── course_detail.html  # Single course view
    ├── register.html       # Registration form
    ├── login.html          # Login form
    ├── dashboard.html      # User dashboard
    ├── success.html        # Enrollment success
    └── contact.html        # Contact form
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/learnhub.git
cd learnhub
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

### 5. Open in Browser
```
http://127.0.0.1:5000
```

> The SQLite database (`learnhub.db`) is created automatically on first run.

---

## 🔄 Application Routes

| Route                  | Method    | Description                  |
|------------------------|-----------|------------------------------|
| `/`                    | GET       | Home page                    |
| `/courses`             | GET       | All courses (filter/search)  |
| `/course/<id>`         | GET       | Course detail page           |
| `/enroll/<id>`         | POST      | Enroll in a course           |
| `/success`             | GET       | Enrollment success page      |
| `/register`            | GET/POST  | User registration            |
| `/login`               | GET/POST  | User login                   |
| `/logout`              | GET       | Logout (clears session)      |
| `/dashboard`           | GET       | User dashboard               |
| `/contact`             | GET/POST  | Contact form                 |

---

## 🧪 Demo Steps

1. Open `http://127.0.0.1:5000`
2. Click **Sign Up** → fill in the form → create account
3. Log in with your credentials
4. Go to **Courses** → click **View Details** on any course
5. Click **Enroll Now** → confirm in the modal
6. View your enrolled courses on the **Dashboard**

---

## 📦 Git Setup

```bash
git init
git add .
git commit -m "Initial commit: LearnHub Online Course Platform"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/learnhub.git
git push -u origin main
```

---

## 🚀 Deployment (Optional — Render)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect GitHub repo
4. Set **Build Command**: `pip install -r requirements.txt`
5. Set **Start Command**: `python app.py`
6. Deploy!

---

## 👨‍💻 Author

Built as a full-stack mini project using Flask + Bootstrap + jQuery.

---

## 📄 License

MIT License
