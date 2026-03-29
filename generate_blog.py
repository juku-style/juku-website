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

        max_tokens=4096,

        messages=[

            {

                "role": "user",

                "content": f"""あなたは学習塩のプロ講師兼セオライターです。

以下の条件でブログ記事を1つ作成してください。

【目的】

・保護者や生徒の悩みを解決する

・検索からの流入を増やす（セオを意識）

・最終的に塔への信頼感を高める

【対象読者】

・小学生～中学生の保護者

・勉強に悩む生徒本人

【記事構成】

① 導入文（共感ベースで150～200文字）

② 見出し（H2相当）を4～6個

③ 各見出しの中に具体的な解説

④ まとめ（行動を促す）

【必須条件】

・抽象論ではなく「現場ベースの具体例」を入れる

・「なぜそうなるのか」を必ず説明する

・難しい言葉は使わず、わかりやすく書く

・1文は長くしすぎない

・PREP法（結論→理由→具体例→まとめ）を意識する

・箇条書きを適度に使う

【差別化要素】

・「実際に多いケース」や「よくある失敗」を入れる

・他の記事にないリアルな視点を入れる

【SEO強化】

・検索されやすいキーワードを自然に含める

・見出しにもキーワードを入れる

・「～とは？」「原因」「対策」など検索意図を意識する

【塔集客要素】

・最後に軽く塔の価値を伝える一文を入れる（押し売りにならない自然な形）

【読みやすさ】

・各見出しごとに結論を最初に書く

【文体・トーン】

・「真面目×ユーモア」を意識する

・冒頭に保護者が共感できる「あるある」エピソードを入れる

・適度に（笑）や！を使い、堅苦すぎない

・保護者が思わずクスッとするような視点や表現を入れる

・でも内容はしっかり役立つ実用的なものにする

・塔の先生が保護者に話しかけるような親しみやすい口調

【禁止事項】

・根拠のない断定

・精神論だけの内容

・薄い一般論

・お堵い教科書のような文章

・AIが書いたとわかるような無機質な表現

【文字数、2000文字程度

今日の日付：{today}

以下のJSON形式のみで返答してください（前後の説明文・```は不要）：

{{

  "title": "SEOを意識した記事タイトル（30文字以内）",

  "tag": "カテゴリ（勉強法／受験対策／保護者向け／学習習慣／モチベーション のいずれか）",

  "summary": "記事の要素80文字以内）",

  "content": "記事本文（2000文字程度、HTML可、見出しは<h2>タグを使用）"

}}"""

            }

        ]

    )

    

    text = message.content[0].text.strip()

    text = re.sub(r"^```json\s*", "", text)

    text = re.sub(r"```json\s*", "", text)

    text = re.sub(r"\s*```$", "", text)

    text = re.sub(r"```\s*", "", text)

    text = text.strip()

    try:

        return json.loads(text)

    except json.JSONDecodeError as e:

        print(f"JSONパースエラー: {e}")

        print(f"受け取ったテキスト（先頭300文字）: {text[:300]}")

        raise

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

    <a href="post_{{post['id']}}.html" class="blog-card">

      <div class="blog-img">{{emoji}}</div>

      <div class="blog-body">

        <div class="blog-meta">

          <span class="blog-tag">{{post['tag']}}</span>

          <span class="blog-date">{{post['date']}}</span>

        </div>

        <h2>{{post['title']}}</h2>

        <p>{{post['summary']}}</p>

      </div>

    </a>"""

    

    with open("blog.html", "r", encoding="utf-8") as f:

        html = f.read()

    

    html = re.sub(

        r'<div class="blog-grid" id="blog-list">.*?</div>',

        f'<div class="blog-grid" id="blog-list">{{cards_html}}\n  </div>',

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

  <title>{{post['title']}} | 学習塩スタイル</title>

  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">

  <style>

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{ font-family: 'Noto Sans JP', sans-serif; color: #1a1a2e; background: #f8faff; padding-bottom: 80px; }}

    nav {{ background: #042C53; padding: 0 2rem; display: flex; align-items: center; justify-content: space-between; height: 64px; }}

    .nav-logo {{ font-family: 'Noto Serif JP', serif; font-size: 18px; color: #fff; text-decoration: none; }}

    .nav-logo span {{ font-size: 10px; color: #c8a96e; display: block; }}

    .nav-btn {{ background: #c8a96e; color: #042C53; border: none; border-radius: 6px; padding: 8px 16px; font-size: 12px; font-weight: 700; cursor: pointer; text-decoration: none; }}

    .post-container {{ max-width: 720px; margin: 0 auto; padding: 3rem 2rem; }}

    .post-hero {{ background: linear-gradient(135deg, #e8f2fd 0%, #c5ddf8 100%); border-radius: 16px; padding: 3rem 2rem; text-align: center; margin-bottom: 2rem; }}

    .post-emoji {{ font-size: 60px; margin-bottom: 1rem; }}

    .post-tag {{ font-size: 12px; background: #185FA5; color: #fff; padding: 4px 14px; border-radius: 99px; display: inline-block; margin-bottom: 1rem; }}

    .post-hero h1 {{ font-family: 'Noto Serif JP', serif; font-size: 24px; color: #042C53; line-height: 1.5; margin-bottom: 0.5rem; }}

    .post-date {{ font-size: 13px; color: #0C447C; }}

    .post-content {{ background: #fff; border: 1px solid #d0e4f7; border-radius: 12px; padding: 2rem; line-height: 1.9; font-size: 15px; color: #333; }}

    .post-content h2 {{ font-size: 18px; font-weight: 700; color: #042C53; margin: 2rem 0 1rem; padding-left: 0.8rem; border-left: 3px solid #185FA5; }}

    .post-content h3 {{ font-size: 16px; font-weight: 700; color: #185FA5; margin: 1.5rem 0 0.8rem; }}

    .post-content p {{ margin-bottom: 1rem; }}

    .post-content ul {{ padding-left: 1.5rem; margin-bottom: 1rem; }}

    .post-content li {{ margin-bottom: 0.4rem; }}

    .back-link {{ display: inline-block; margin-top: 2rem; color: #185FA5; text-decoration: none; font-size: 14px; }}

    .fixed-banner {{ position: fixed; bottom: 0; left: 0; right: 0; background: #042C53; border-top: 1px solid rgba(255,255,255,0.1); padding: 12px 2rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; z-index: 300; }}

    .banner-text strong {{ font-size: 14px; color: #fff; display: block; }}

    .banner-text span {{ font-size: 11px; color: #a0b8d0; }}

    .banner-btn {{ background: #c8a96e; color: #042C53; border: none; border-radius: 6px; padding: 10px 20px; font-size: 13px; font-weight: 700; cursor: pointer; white-space: nowrap; text-decoration: none; }}

    footer {{ background: #042C53; padding: 2rem; text-align: center; margin-top: 3rem; }}

    footer p {{ font-size: 13px; color: #7ab0d4; }}

  </style>

</head>

<body>

<nav>

  <a href="index.html" class="nav-logo">学習塩スタイル<span>JUKU STYLE</span></a>

  <a href="members.html" class="nav-btn">生徒・保護者ログイン</a>

</nav>

<div class="post-container">

  <div class="post-hero">

    <div class="post-emoji">{{emoji}}</div>

    <span class="post-tag">{{post['tag']}}</span>

    <h1>{{post['title']}}</h1>

    <p class="post-date">{{post['date']}}</p>

  </div>

  <div class="post-content">{{content_html}}</div>

  <a href="blog.html" class="back-link">← ブログ一覧に戻る</a>

</div>

<div class="fixed-banner">

  <div class="banner-text">

    <strong>🎓体験授業 受付中！</strong>

    <span>まずはお気軽にお問い合わせください</span>

  </div>

  <a href="index.html" class="banner-btn">入塔の流れを見る</a>

</div>

<footer>

  <p>© 2025 学習塩スタイル</p>

</footer>

</body>

</html>"""

    

    with open(f"post_{{post['id']}}.html", "w", encoding="utf-8") as f:

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

    

    print(f"✅ 記事を生成しました：{{new_post['title']}}")

if __name__ == "__main__":

    main()
