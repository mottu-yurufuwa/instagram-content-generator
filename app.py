import os
import requests
import base64
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)

# API設定
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def generate_image_prompt(keyword):
    """Claude APIを使用して画像生成プロンプトを作成"""
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01'
    }
    
    prompt = f"""
キーワード「{keyword}」を元に、DALL-E 3で美しい画像を生成するための詳細な英語プロンプトを作成してください。
以下の要素を含めてください：
- 視覚的な詳細（色、照明、構図）
- 芸術スタイル
- 雰囲気や感情
- 技術的な品質指定

200語程度の英語プロンプトで回答してください。
"""
    
    data = {
        'model': 'claude-3-sonnet-20240229',
        'max_tokens': 300,
        'messages': [{'role': 'user', 'content': prompt}]
    }
    
    try:
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=data
        )
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        response.raise_for_status()
        return response.json()['content'][0]['text'].strip()
    except Exception as e:
        print(f"Error details: {str(e)}")
        return f"エラーが発生しました: {str(e)}"

def generate_image_with_dalle3(prompt):
    """DALL-E 3 APIを使用して画像を生成"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    
    data = {
        'model': 'dall-e-3',
        'prompt': prompt,
        'n': 1,
        'size': '1024x1024',
        'quality': 'standard'
    }
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/images/generations',
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()['data'][0]['url']
    except Exception as e:
        return None

def generate_instagram_caption(keyword, image_prompt):
    """Claude APIを使用してInstagramキャプションを生成"""
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01'
    }
    
    prompt = f"""
キーワード「{keyword}」と画像プロンプト「{image_prompt}」を元に、Instagram用の詩的で魅力的なキャプションを作成してください。

以下の形式で回答してください：
1. 日本語キャプション（3-4行の詩的な文章）
2. 英語キャプション（3-4行の詩的な文章）
3. 関連するハッシュタグ（日本語・英語混合で10-15個）

感情的で美しい表現を使い、Instagram映えする内容にしてください。
"""
    
    data = {
        'model': 'claude-3-sonnet-20240229',
        'max_tokens': 500,
        'messages': [{'role': 'user', 'content': prompt}]
    }
    
    try:
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=data
        )
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        response.raise_for_status()
        return response.json()['content'][0]['text'].strip()
    except Exception as e:
        print(f"Error details: {str(e)}")
        return f"エラーが発生しました: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        keyword = data.get('keyword', '').strip()
        
        if not keyword:
            return jsonify({'error': 'キーワードを入力してください'}), 400
        
        # Step 1: Claude APIで画像生成プロンプトを作成
        image_prompt = generate_image_prompt(keyword)
        if image_prompt.startswith('エラーが発生しました'):
            return jsonify({'error': image_prompt}), 500
        
        # Step 2: DALL-E 3で画像を生成
        image_url = generate_image_with_dalle3(image_prompt)
        if not image_url:
            return jsonify({'error': '画像生成に失敗しました'}), 500
        
        # Step 3: Claude APIでInstagramキャプションを生成
        caption = generate_instagram_caption(keyword, image_prompt)
        if caption.startswith('エラーが発生しました'):
            return jsonify({'error': caption}), 500
        
        return jsonify({
            'keyword': keyword,
            'image_prompt': image_prompt,
            'image_url': image_url,
            'caption': caption
        })
        
    except Exception as e:
        return jsonify({'error': f'予期しないエラーが発生しました: {str(e)}'}), 500

if __name__ == '__main__':
    # APIキーの確認
    if not CLAUDE_API_KEY or not OPENAI_API_KEY:
        print("警告: .envファイルにCLAUDE_API_KEYとOPENAI_API_KEYを設定してください")
    
    app.run(debug=True, host='0.0.0.0', port=5000)