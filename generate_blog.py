import anthropic
import json
import os
import re
from datetime import datetime

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

EMOJIS = ["✏️", "💬", "📚", "🌟", "🎯", "🎮", "🌈", "🎵"]

def generate_blog_post():
    today = datetime.now().strftime("%Y年%m月%d日")
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"""小学生向けの英会話ブログ記事を1つ作成してください。

以下のJSON形式のみで返答してください（他の文章は不要）：
{{
  "title": "記事タイトル（20文字以内）",
  "tag": "カテゴリ（例：今週のフレーズ／会話シナリオ／文法解説／英語豆知識）",
  "summary": "記事の要約（60文字以内）",
  "content": "記事本文（400〜600文字、小学生にわかりやすく、英語フレーズを含む）"
}}

テーマ：小学生が日常で使える英会話フレーズ
対象：小学生とその保護者
口調：親しみやすく楽しい
今日の日付：{today}"""
            }
        ]
    )
    
    text = message.content[0].text.strip()
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    return json.loads(text)

def load_blog_posts():
    if os.path.exists("blog_posts.json"):
        with open("blog_posts.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_blog_posts(posts):
    with open("blog_posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def update_blog_html(posts):
    cards_html = ""
    for i, post in enumerate(posts):
        emoji = EMOJIS[i % len(EMOJIS)]
        cards_html += f"""
    <a href="post_{post['id']}.html" class="blog-card">
      <div class="blog-img">{emoji}</div>
      <div class="blog-body">
        <div class="blog-meta">
          <span class="blog-tag">{post['tag']}</span>
          <span class="blog-date">{post['date']}</span>
        </div>
        <h2>{post['title']}</h2>
        <p>{post['summary']}</p>
      </div>
    </a>"""
    
    with open("blog.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    html = re.sub(
        r'<div class="blog-grid" id="blog-list">.*?</div>',
        f'<div class="blog-grid" id="blog-list">{cards_html}\n  </div>',
        html,
        flags=re.DOTALL
    )
    
    with open("blog.html", "w", encoding="utf-8") as f:
        f.write(html)

def create_post_page(post):
    emoji = EMOJIS[post.get('index', 0) % len(EMOJIS)]
    content_html = post['content'].replace('\n', '<br>')
    
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{post['title']} | Starlight English</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Noto Sans JP', sans-serif; color: #1a1a2e; background: #f8faff; }}
    nav {{ background: #fff; border-bottom: 1px solid #e0eaf5; padding: 0 2rem; display: flex; align-items: center; justify-content: space-between; height: 60px; }}
    .nav-logo {{ font-size: 20px; font-weight: 700; color: #185FA5; text-decoration: none; }}
    .nav-logo span {{ font-size: 11px; color: #888; display: block; font-weight: 400; }}
    .nav-btn {{ background: #185FA5; color: #fff; border: none; border-radius: 8px; padding: 8px 18px; font-size: 13px; cursor: pointer; text-decoration: none; }}
    .post-container {{ max-width: 720px; margin: 0 auto; padding: 3rem 2rem; }}
    .post-hero {{ background: linear-gradient(135deg, #e8f2fd 0%, #c5ddf8 100%); border-radius: 16px; padding: 3rem 2rem; text-align: center; margin-bottom: 2rem; }}
    .post-emoji {{ font-size: 60px; margin-bottom: 1rem; }}
    .post-tag {{ font-size: 12px; background: #185FA5; color: #fff; padding: 4px 14px; border-radius: 99px; display: inline-block; margin-bottom: 1rem; }}
    .post-hero h1 {{ font-size: 24px; font-weight: 700; color: #042C53; line-height: 1.5; margin-bottom: 0.5rem; }}
    .post-date {{ font-size: 13px; color: #0C447C; }}
    .post-content {{ background: #fff; border: 1px solid #d0e4f7; border-radius: 12px; padding: 2rem; line-height: 1.8; font-size: 15px; color: #333; }}
    .back-link {{ display: inline-block; margin-top: 2rem; color: #185FA5; text-decoration: none; font-size: 14px; }}
    footer {{ background: #042C53; padding: 2rem; text-align: center; margin-top: 3rem; }}
    footer p {{ font-size: 13px; color: #7ab0d4; }}
  </style>
</head>
<body>
<nav>
  <a href="index.html" class="nav-logo">⭐ Starlight English<span>福山市の小学生英会話スクール</span></a>
  <a href="members.html" class="nav-btn">生徒・保護者ログイン</a>
</nav>
<div class="post-container">
  <div class="post-hero">
    <div class="post-emoji">{emoji}</div>
    <span class="post-tag">{post['tag']}</span>
    <h1>{post['title']}</h1>
    <p class="post-date">{post['date']}</p>
  </div>
  <div class="post-content">{content_html}</div>
  <a href="blog.html" class="back-link">← ブログ一覧に戻る</a>
</div>
<footer>
  <p>© 2025 Starlight English — 福山市の小学生英会話スクール</p>
</footer>
</body>
</html>"""
    
    with open(f"post_{post['id']}.html", "w", encoding="utf-8") as f:
        f.write(html)

def main():
    print("ブログ記事を生成中...")
    
    post_data = generate_blog_post()
    
    posts = load_blog_posts()
    
    new_post = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "title": post_data["title"],
        "tag": post_data["tag"],
        "summary": post_data["summary"],
        "content": post_data["content"],
        "date": datetime.now().strftime("%Y年%m月%d日"),
        "index": len(posts)
    }
    
    posts.insert(0, new_post)
    posts = posts[:20]
    
    for i, post in enumerate(posts):
        post['index'] = i
    
    save_blog_posts(posts)
    update_blog_html(posts)
    create_post_page(new_post)
    
    print(f"✅ 記事を生成しました：{new_post['title']}")

if __name__ == "__main__":
    main()
