# AI Web Consultant (Local Business Edition)

山形・仙台エリアの地方企業や店舗のDXを支援するための、「AI Web戦略立案ツール」です。
ウェブ解析士の思考プロセスをAIに実装し、実務でそのまま使える提案書を作成します。

## 主な機能
- **AI戦略レポート生成**: 企業名と悩みを入力するだけで、3C分析やKPI設計を含む詳細なレポートを生成。
- **プロ仕様のPDF出力**: html2pdf.jsを活用し、クライアントにそのまま提出可能なPDF形式で保存。
- **高度なプロンプト設計**: ウェブ解析士のフレームワークに基づいた構造的な回答を実現。
- **レスポンシブデザイン**: PCだけでなく、タブレットやスマホからも操作可能なUI。

## 使用技術 (Tech Stack)
- **Backend**: Python 3.10 / Flask
- **AI API**: Google Gemini API (gemini-flash-latest)
- **Frontend**: JavaScript (Vanilla JS), HTML5, CSS3
- **Libraries**: Marked.js (Markdown解析), html2pdf.js (PDF生成), Font Awesome (アイコン)

## セキュリティ・こだわり
- **環境変数の管理**: `python-dotenv` を使用し、APIキーをコードから分離。`.gitignore` により機密情報の漏洩を防止しています。
- **デバッグ実績**: 開発過程で直面したAPIのクォータ制限（429エラー）やモデル名の不一致（404エラー）を、自らテストスクリプトを作成して解決しました。
- **地域への想い**: 仙台の「村上屋餅店」様のような、歴史ある老舗がデジタルを活用して若年層と繋がるための架け橋となるツールを目指しました。

## 使い方 (Local Setup)
1. リポジトリをクローン
2. `.env` ファイルを作成し、`GENAI_API_KEY` を設定
3. `pip install -r requirements.txt` で依存関係をインストール
4. `python app.py` を実行して `http://localhost:5000` にアクセス