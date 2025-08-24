import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# API設定
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def generate_image_prompt(keyword, style='v4b'):
    """OpenAI GPTを使用して画像生成プロンプトを作成"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    
    # 画風別のスタイル定義
    style_definitions = {
        'v4b': {
            'description': '高発色・コントラスト強め・クリーンな線画の"V4B風味"',
            'characteristics': '- crisp clean lineart, high contrast, vivid yet natural colors\n- semi-realistic shading, gentle bloom, subtle film grain\n- soft background bokeh, depth layering, tidy edges\n- skin tones clean, highlights specular but controlled'
        },
        'anime': {
            'description': 'ソフトなアニメスタイル・パステルカラー',
            'characteristics': '- soft anime art style, gentle pastel color palette\n- smooth cell shading, minimal shadows, bright highlights\n- clean simplified features, large expressive eyes\n- dreamy atmosphere, soft lighting, ethereal quality'
        },
        'realistic': {
            'description': '写実的・自然な照明',
            'characteristics': '- photorealistic rendering, natural skin textures\n- realistic lighting and shadows, accurate proportions\n- detailed facial features, natural color tones\n- depth of field, environmental details, lifelike quality'
        },
        'illustration': {
            'description': 'デジタルアート・筆のタッチ',
            'characteristics': '- digital painting style, visible brush strokes\n- artistic interpretation, stylized features\n- rich color blending, painterly textures\n- creative composition, artistic flair, expressive style'
        },
        'watercolor': {
            'description': '水彩画・ソフトなエッジ',
            'characteristics': '- watercolor painting technique, soft flowing edges\n- transparent color washes, bleeding effects\n- delicate color transitions, paper texture visible\n- gentle, dreamy atmosphere, light and airy feel'
        },
        'oilpainting': {
            'description': '油絵のテクスチャ・豊かな色彩',
            'characteristics': '- oil painting texture, thick impasto brushwork\n- rich saturated colors, dramatic lighting\n- classical painting techniques, artistic depth\n- textured canvas surface, masterful color mixing'
        }
    }
    
    selected_style = style_definitions.get(style, style_definitions['v4b'])
    
    prompt = f"""あなたはアニメ調画像のプロンプト設計アシストです。
キーワード「{keyword}」から、{selected_style['description']}でDALL-E 3向けのプロンプトを作成してください。

スタイルの方向性：
{selected_style['characteristics']}

以下の要素を含めた詳細な英語プロンプトを作成してください：
- キーワードを基にした具体的なシーン設定
- 指定された画風の美しい表現
- 適切なライティング（soft rim light, backlight, bounced light）
- スタイルに適したカラーパレット
- 構図とカメラアングル（3/4 view, rule of thirds等）
- 高品質指定（指定スタイルに応じた品質表現）

実在のアーティスト名や特定スタイル名は使わず、表現特徴で言語化してください。
Instagram映えする美しい結果になるよう、約200-250語の英語プロンプトで回答してください。"""
    
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 300
    }
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
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
        'quality': 'hd',
        'style': 'vivid'
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
    """OpenAI GPTを使用してInstagramキャプションを生成"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    
    prompt = f"""Based on the keyword "{keyword}" and image prompt "{image_prompt}", create an engaging Instagram caption.

Please format your response EXACTLY as follows (without numbers):

[Japanese caption - 3-4 lines of poetic text]

[English caption - 3-4 lines of poetic text]

[Related hashtags - 10-15 hashtags in Japanese and English, all on one line]

Use emotional and beautiful expressions that are Instagram-worthy. Do NOT include numbers, bullets, or any formatting marks. Make it ready to copy and paste directly to Instagram."""
    
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 500
    }
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        keyword = data.get('keyword', '').strip()
        style = data.get('style', 'v4b')
        
        if not keyword:
            return jsonify({'error': 'キーワードを入力してください'}), 400
        
        # Step 1: OpenAI GPTで画像生成プロンプトを作成
        image_prompt = generate_image_prompt(keyword, style)
        if image_prompt.startswith('エラーが発生しました'):
            return jsonify({'error': image_prompt}), 500
        
        # Step 2: DALL-E 3で画像を生成
        image_url = generate_image_with_dalle3(image_prompt)
        if not image_url:
            return jsonify({'error': '画像生成に失敗しました'}), 500
        
        # Step 3: OpenAI GPTでInstagramキャプションを生成
        caption = generate_instagram_caption(keyword, image_prompt)
        if caption.startswith('エラーが発生しました'):
            return jsonify({'error': caption}), 500
        
        return jsonify({
            'keyword': keyword,
            'style': style,
            'image_prompt': image_prompt,
            'image_url': image_url,
            'caption': caption
        })
        
    except Exception as e:
        return jsonify({'error': f'予期しないエラーが発生しました: {str(e)}'}), 500

if __name__ == '__main__':
    if not OPENAI_API_KEY:
        print("警告: .envファイルにOPENAI_API_KEYを設定してください")
    
    app.run(debug=True, host='0.0.0.0', port=5000)