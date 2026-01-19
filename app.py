import os
import sqlite3  # ← 追加：標準ライブラリなのでインストール不要
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

# API設定
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

# --- データベースの準備 ---
def init_db():
    # データベースファイル（database.db）に接続
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # テーブル（倉庫の棚）を作る
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            biz_name TEXT,
            goal TEXT,
            advice TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

# アプリ起動時にデータベースを初期化
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consult', methods=['POST'])
def consult():
    try:
        data = request.json
        biz_name = data.get('businessName')
        biz_goal = data.get('goal')
        
        prompt = (
            f"あなたはプロのウェブ解析士です。企業名 {biz_name}、"
            f"悩み {biz_goal} に対して戦略を立ててください。"
        )

        response = model.generate_content(prompt)
        advice_text = response.text

        # ★追加：AIの回答をデータベースに保存する
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reports (biz_name, goal, advice, created_at) VALUES (?, ?, ?, ?)",
            (biz_name, biz_goal, advice_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()
        
        return jsonify({"advice": advice_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ★追加：保存された履歴を取得する機能
@app.route('/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # 新しい順に取得
    cursor.execute("SELECT biz_name, created_at, advice FROM reports ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    # リスト形式にして返す
    history = [{"biz_name": r[0], "date": r[1], "advice": r[2]} for r in rows]
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)