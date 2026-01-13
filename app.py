import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# .env ファイルから設定（APIキーなど）を読み込む
load_dotenv()

app = Flask(__name__)

# 環境変数からAPIキーを取得
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

# あなたの環境で動作確認が取れたモデル名を使用
model = genai.GenerativeModel('gemini-flash-latest')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consult', methods=['POST'])
def consult():
    try:
        data = request.json
        biz_name = data.get('businessName')
        biz_goal = data.get('goal')
        
        # ウェブ解析士の視点を組み込んだプロフェッショナルなプロンプト
        prompt = (
            f"あなたは地方企業のDXを支援する超一流のウェブ解析士兼デジタルマーケティング戦略家です。\n\n"
            f"【クライアント情報】\n"
            f"企業・店舗名: {biz_name}\n"
            f"現在の課題・目標: {biz_goal}\n\n"
            f"【指示】\n"
            f"プロの視点から、以下の4つの項目で具体的かつ実行可能な戦略レポートを作成してください。\n"
            f"1. **現状分析 (3C分析的視点)**: 市場における強みと機会を特定してください。\n"
            f"2. **ターゲットとカスタマージャーニー**: 誰に、どのタイミングでアプローチすべきか具体的に提示してください。\n"
            f"3. **具体的施策 (3本柱)**: SNS活用、SEO、UI/UX改善、広告などから、優先度の高いものを3つ提案してください。\n"
            f"4. **成功を測る指標 (KPI)**: 何を数値目標にすべきか設定してください。\n\n"
            f"【出力ルール】\n"
            f"・専門用語を使いつつも、経営者に伝わる丁寧な言葉遣い（です・ます調）で。\n"
            f"・Markdown形式で見出し、箇条書き、太字を多用して読みやすくしてください。\n"
            f"・山形や仙台といった地域特性を考慮できる場合は、そのエッセンスを加えてください。"
        )

        # AIに問い合わせ
        response = model.generate_content(prompt)
        
        return jsonify({"advice": response.text})

    except Exception as e:
        # エラーが発生した場合は詳細をブラウザ側に返す
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # サーバーの起動
    app.run(debug=True, port=5000)