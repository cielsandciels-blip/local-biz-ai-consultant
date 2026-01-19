# AI Web 戦略コンサルタント (Local Biz AI Consultant)

ウェブ解析士の視点と生成AIを融合させた、中小企業・店舗向けのWeb戦略立案支援ツールです。
ユーザーごとの診断履歴管理と、セキュアな認証機能を備えたフルスタックなWebアプリケーションとして開発しました。

## 特徴 (Features)

1. **AI戦略コンサルティング**: Google Gemini APIを活用し、企業情報と目標に基づいた具体的なWeb戦略を数秒で生成。
2. **ユーザー認証システム**: `Flask-Login` を使用した会員登録・ログイン機能。パスワードはハッシュ化（`Werkzeug`）して安全に保存。
3. **個別履歴管理**: ユーザーごとに過去の診断結果をSQLiteデータベースに保存。いつでも過去の提案を振り返ることが可能。
4. **モダンなUI/UX**: グラスモーフィズムを取り入れた清潔感のあるログイン画面と、レスポンシブな診断ダッシュボード。
5. **PDFレポート出力**: 診断結果をその場でPDF化し、オフラインでの確認や共有に対応。

## 🛠 使用技術 (Tech Stack)

- **Backend**: Python 3.10 / Flask
- **AI API**: Google Gemini API (gemini-flash-latest)
- **Database**: SQLite (会員情報および診断履歴の永続化)
- **Authentication**: Flask-Login, Werkzeug (パスワードハッシュ化)
- **Security**: python-dotenv (環境変数によるAPIキー管理)
- **Frontend**: JavaScript (Vanilla JS), HTML5, CSS3
- **Design**: モダンなUIデザイン (CSS Grid/Flexbox)

## プロジェクトの構造
- `app.py`: メインのバックエンドロジック（認証・AI連携・DB操作）
- `database.db`: ユーザー情報および履歴を格納するDB
- `templates/`: HTMLファイル（ログイン、登録、メイン画面）
- `static/`: CSSおよびJavaScriptファイル
- `requirements.txt`: 実行に必要なライブラリ一覧

## 開発の背景
「ウェブ解析士」として学んだ専門知識を、より手軽に、かつ安全に多くの企業に届けるためのツールとして開発しました。単にAIを呼び出すだけでなく、実務レベルのセキュリティ（認証機能や環境変数管理）を実装し、継続的に利用できるサービス形態を目指しました。

## 使い方 (Local Setup)
1. リポジトリをクローン
2. `.env` ファイルを作成し、`GENAI_API_KEY` を設定
3. `pip install -r requirements.txt` で依存関係をインストール
4. `python app.py` を実行して `http://localhost:5000` にアクセス