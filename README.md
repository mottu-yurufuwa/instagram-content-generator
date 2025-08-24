インスタファンづくり画像生成自動化ツール

キーワードを入力するだけで、OpenAI API (GPT-3.5 + DALL-E 3) を使って美しい画像とInstagram用キャプションを自動生成するWebアプリケーションです。

✨ 機能

キーワード入力
テキストボックスにキーワードを入力するだけ

画像生成プロンプト作成
GPT-3.5が詳細な英語プロンプトを生成

画像生成
DALL-E 3がHD品質の画像を生成

Instagramキャプション生成
GPT-3.5が日本語＋英語キャプション＋ハッシュタグを生成

ワンクリックコピー
キャプションを1クリックでコピー可能

🛠️ セットアップ手順

1. 依存関係インストール

pip install -r requirements.txt

2. 環境変数の設定

.env.example をコピーして .env を作成してください：

cp .env.example .env

.env を開いて、自分の OpenAI APIキー を入力します：

OPENAI\_API\_KEY=your\_openai\_api\_key

Claude APIキーは任意（未使用の場合は空でOK）
3. APIキー取得方法

OpenAI API: https://platform.openai.com/

無料枠あり。追加利用は従量課金。

※ Claude APIは本ツールでは不要（オプション扱い）です。

🚀 アプリ起動

python app.py

ブラウザで以下にアクセスしてください：

http://localhost:5000

💡 使用例

Webページにアクセス

テキストボックスにキーワードを入力（例：「夏の少女」）

「✨ 生成する」をクリック

数秒待つと、画像とキャプションが自動生成されます

📂 プロジェクト構造

インスタファンづくり画像生成自動化ツール/
├── app.py # メインアプリケーション
├── app\_simple.py # Claudeなしバージョン（推奨）
├── requirements.txt # 依存関係
├── .env.example # 環境変数テンプレート
├── README.md # このファイル
├── templates/
│ └── index.html # HTMLテンプレート
└── static/
└── style.css # CSSスタイル

💰 コスト情報（目安）

GPT-3.5: キャプション生成 → ほぼ無料

DALL-E 3 HD: 1画像 = 約 $0.08（12円程度）

1日1投稿 × 30日 ≒ 月500円前後

⚠️ 注意事項

.env のAPIキーは絶対に公開しないでください

画像生成にはOpenAI APIのクレジットが消費されます

本ZIPの再配布・転売は禁止です

