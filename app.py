import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-123' # セッション管理用のカギ

# --- Gemini APIの設定 ---
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

# --- Flask-Loginの設定 ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # ログインしていない時に飛ばすページ

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data[0], user_data[1])
    return None

# --- データベース初期化 ---
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # 会員名簿
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    # 診断履歴（user_idを追加）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            biz_name TEXT,
            goal TEXT,
            advice TEXT,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- ルーティング（各ページの設定） ---

@app.route('/')
@login_required # ログインしていないと見れないようにする
def index():
    return render_template('index.html', user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_pw = generate_password_hash(password)
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_pw))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "そのユーザー名は既に使われています。"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and check_password_hash(user_data[2], password):
            user = User(user_data[0], user_data[1])
            login_user(user)
            return redirect(url_for('index'))
        else:
            return "ユーザー名またはパスワードが違います。"
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/consult', methods=['POST'])
@login_required
def consult():
    try:
        data = request.json
        biz_name = data.get('businessName')
        biz_goal = data.get('goal')
        
        prompt = f"あなたはプロのウェブ解析士です。企業名 {biz_name}、悩み {biz_goal} に対して戦略を立ててください。"
        response = model.generate_content(prompt)
        advice_text = response.text

        # ログイン中のユーザーIDと一緒に保存する
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reports (user_id, biz_name, goal, advice, created_at) VALUES (?, ?, ?, ?, ?)",
            (current_user.id, biz_name, biz_goal, advice_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()
        
        return jsonify({"advice": advice_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/history', methods=['GET'])
@login_required
def get_history():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # ログイン中のユーザーの履歴だけを取得する
    cursor.execute("SELECT biz_name, created_at, advice FROM reports WHERE user_id = ? ORDER BY id DESC", (current_user.id,))
    rows = cursor.fetchall()
    conn.close()
    
    history = [{"biz_name": r[0], "date": r[1], "advice": r[2]} for r in rows]
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)