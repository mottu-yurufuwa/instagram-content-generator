# インスタファンづくり画像生成自動化ツール

キーワードを入力するだけで、OpenAI API (GPT-3.5 + DALL-E 3) を使って美しい画像とInstagram用キャプションを自動生成するWebアプリケーションです。

🌐 **Webで無料公開** - Vercelを使って誰でも簡単にWebアプリとして公開できます！

## ✨ 機能

- **キーワード入力**: テキストボックスにキーワードを入力するだけ
- **画像風選択**: V4B風、アニメ風、写実的など6種類の画風から選択
- **画像生成プロンプト作成**: GPT-3.5が詳細な英語プロンプトを生成
- **画像生成**: DALL-E 3がHD品質の画像を生成
- **Instagramキャプション生成**: GPT-3.5が日本語＋英語キャプション＋ハッシュタグを生成
- **ワンクリックコピー**: キャプションを1クリックでコピー可能

## 🚀 Web公開手順（推奨）

### 必要なもの
- GitHubアカウント（無料）
- Vercelアカウント（無料）
- OpenAI APIキー

### Step 1: OpenAI APIキーを取得
1. https://platform.openai.com/ にアクセス
2. アカウント作成・ログイン
3. 「API keys」から新しいAPIキーを作成
4. 作成したAPIキーをコピー（後で使用）

**💰 料金**: 無料枠あり、DALL-E 3は1画像約12円

### Step 2: GitHubにアップロード
1. **GitHubアカウント作成**: https://github.com でアカウント作成
2. **新しいリポジトリ作成**: 「New repository」をクリック
   - Repository name: `instagram-content-generator`（任意）
   - Public/Private を選択
   - 「Create repository」をクリック

3. **ファイルをアップロード**:
   - フォルダ内のすべてのファイルを選択してドラッグ&ドロップ
   - コミットメッセージ: `Initial commit`
   - 「Commit changes」をクリック

### Step 3: Vercelでデプロイ
1. **Vercelアカウント作成**: https://vercel.com にアクセス
2. 「Continue with GitHub」でGitHubアカウントでログイン
3. **プロジェクト作成**:
   - 「Add New...」→「Project」をクリック
   - 先ほど作成したGitHubリポジトリを選択
   - 「Import」をクリック

4. **環境変数設定**:
   - 「Environment Variables」セクションで以下を追加:
     - **Name**: `OPENAI_API_KEY`
     - **Value**: Step 1で取得したAPIキー
   - 「Add」→「Deploy」をクリック

5. **完了**: 3-5分でデプロイ完了。Vercelが提供するURLでアクセス可能！

---

## 🛠️ ローカル開発手順

### 1. 依存関係インストール
```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定
```bash
cp .env.example .env
```

`.env` ファイルを開いて、OpenAI APIキーを入力：
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. アプリ起動
```bash
python app.py
```

ブラウザで http://localhost:5000 にアクセス

## 💡 使用方法

1. Webページにアクセス
2. テキストボックスにキーワードを入力（例：「夏の少女」）
3. 画風を選択（V4B風、アニメ風など）
4. 「✨ 生成する」をクリック
5. 数秒待つと、画像とキャプションが自動生成されます
6. キャプションをコピーしてInstagramに投稿！

## 📂 プロジェクト構造

```
instagram-content-generator/
├── app.py              # メインアプリケーション
├── requirements.txt    # 依存関係
├── .env.example       # 環境変数テンプレート
├── vercel.json        # Vercel設定
├── runtime.txt        # Pythonバージョン
├── templates/
│   └── index.html     # HTMLテンプレート
└── static/
    └── style.css      # CSSスタイル
```

## 💰 コスト情報（目安）

- **GPT-3.5**: キャプション・プロンプト生成 → ほぼ無料
- **DALL-E 3 HD**: 1画像 = 約 $0.08（12円程度）
- **1日1投稿 × 30日**: 月500円前後

## 🔧 トラブルシューティング

### よくある問題と解決方法

**❌ Vercelビルドエラー「runtime requires valid version」**
- → `vercel.json`の設定が正しくない場合があります
- 解決方法: リポジトリの`vercel.json`を確認してください

**❌ 「OpenAI API error」**
- → APIキーが正しく設定されていない
- 解決方法: Vercelの環境変数設定を再確認してください

**❌ 画像生成が失敗する**
- → OpenAI APIの残高不足の可能性
- 解決方法: OpenAIアカウントでクレジット残高を確認してください

**❌ GitHubアップロードでファイルが見つからない**
- → `.gitignore`で除外されている可能性
- 解決方法: 重要なファイル（`.env`は除く）がすべて含まれているか確認してください

### サポート

問題が解決しない場合は、GitHubのIssuesでお気軽にお尋ねください。

## ⚠️ 注意事項

- **APIキーの管理**: `.env`ファイルのAPIキーは絶対に公開しないでください
- **コスト管理**: 画像生成にはOpenAI APIのクレジットが消費されます
- **利用規約**: OpenAI APIの利用規約を遵守してください

