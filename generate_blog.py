import anthropic
import json
import os
import re
from datetime import datetime

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

EMOJIS = ["✏️", "💬", "📚", "🌟", "🎯", "🎮", "🌈", "🎵"]

def generate_blog_post():
    today = datetime.now().strftime("%Y年%m月%d日")
    
    prompt = """あなたは学習塾のプロ講師兼ライターです。
以下の条件でブログ記事を1つ作成してください。

【目的】
・保護者や生徒の悩みを解決する
・読んだ人が「なるほど」「ちょっとわかる」と感じる記事
・最終的に塾への信頼感を高める

【対象読者】
・小学生〜中学生の保護者
・勉強に悩む生徒本人

【テーマの選び方】
・保護者や生徒がよく感じる悩みや場面からテーマを選ぶ
・例：「子どもが勉強しない」「成績が上がらない」「やる気が続かない」など

【記事構成】
① 保護者や生徒がよく感じる悩みや場面を提示（共感ベースで150〜200文字）
② 「ただ、〜」や「でも、〜」で視点をズラす
③ 日常的・具体的な例（あるある）を1〜2個入れる
④ 本質的な一文（少し刺さる表現）
⑤ 余韻のある締め（断定しすぎない）
⑥ 各見出し（H2）を4〜6個使って構成する

【トーン】
・真面目 × ユーモア（軽くクスッとする程度）
・批判や否定はせず、共感と考察ベース
・少しだけ文学的（比喩・余韻あり）
・上から目線にならない
・塾の先生が保護者に話しかけるような親しみやすい口調

【ユーモア】
・人間らしい感情や思い出に対する軽い皮肉
・制度や誰かを否定しない
・「ちょっと分かる」が出るレベルに抑える

【必須条件】
・抽象論ではなく現場ベースの具体例を入れる
・なぜそうなるのかを必ず説明する
・難しい言葉は使わずわかりやすく書く
・1文は長くしすぎない
・箇条書きを適度に使う

【SEO強化】
・検索されやすいキーワードを自然に含める
・見出しにもキーワードを入れる

【塾集客要素】
・最後に軽く塾の価値を伝える一文を入れる（押し売りにならない自然な形）

【禁止事項】
・根拠のない断定
・精神論だけの内容
・薄い一般論
・お堅い教科書のような文章
・AIが書いたとわかるような無機質な表現

【文字数】2000文字程度

今日の日付：""" + today + """

以下のJSON形式のみで返答してください（前後の説明文・```は不要）：
{
  "title": "SEOを意識した記事タイトル（30文字以内）",
  "tag": "カテゴリ（勉強法／受験対策／保護者向け／学習習慣／モチベーション のいずれか）",
  "summary": "記事の要約（80文字以内）",
  "content": "記事本文（2000文字程度、HTML可、見出しは<h2>タグを使用）"
}"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": prompt
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
        print("JSONパースエラー: " + str(e))
        print("受け取ったテキスト（先頭300文字）: " + text[:300])
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
        pid = post['id']
        ptag = post['tag']
        pdate = post['date']
        ptitle = post['title']
        psummary = post['summary']
        cards_html += "\n    <a href=\"post_" + pid + ".html\" class=\"blog-card\">\n      <div class=\"blog-img\">" + emoji + "</div>\n      <div class=\"blog-body\">\n        <div class=\"blog-meta\">\n          <span class=\"blog-tag\">" + ptag + "</span>\n          <span class=\"blog-date\">" + pdate + "</span>\n        </div>\n        <h2>" + ptitle + "</h2>\n        <p>" + psummary + "</p>\n      </div>\n    </a>"
    
    with open("blog.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    new_grid = '<div class="blog-grid" id="blog-list">' + cards_html + "\n  </div>"
    
    if '<div class="blog-grid" id="blog-list">' in html:
        start = html.find('<div class="blog-grid" id="blog-list">')
        end = html.find('</div>', start) + len('</div>')
        html = html[:start] + new_grid + html[end:]
    
    with open("blog.html", "w", encoding="utf-8") as f:
        f.write(html)

def create_post_page(post):
    emoji = EMOJIS[post.get('index', 0) % len(EMOJIS)]
    pid = post['id']
    ptitle = post['title']
    ptag = post['tag']
    pdate = post['date']
    pcontent = post['content'].replace('\n', '<br>')
    
    html = "<!DOCTYPE html>\n"
    html += "<html lang=\"ja\">\n"
    html += "<head>\n"
    html += "  <meta charset=\"UTF-8\">\n"
    html += "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
    html += "  <title>" + ptitle + " | 学習塾スタイル</title>\n"
    html += "  <link href=\"https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&family=Noto+Sans+JP:wght@400;500;700&display=swap\" rel=\"stylesheet\">\n"
    html += "  <style>\n"
    html += "    * { box-sizing: border-box; margin: 0; padding: 0; }\n"
    html += "    body { font-family: 'Noto Sans JP', sans-serif; color: #1a1a2e; background: #f8faff; padding-bottom: 80px; }\n"
    html += "    nav { background: #4DC8E8; padding: 0 2rem; display: flex; align-items: center; justify-content: space-between; height: 64px; }\n"
    html += "    .nav-logo { font-family: 'Noto Serif JP', serif; font-size: 18px; color: #fff; text-decoration: none; }\n"
    html += "    .nav-logo span { font-size: 10px; color: #fff; display: block; opacity: 0.85; }\n"
    html += "    .nav-btn { background: #fff; color: #1DA8CC; border: none; border-radius: 6px; padding: 8px 16px; font-size: 12px; font-weight: 700; cursor: pointer; text-decoration: none; }\n"
    html += "    .post-container { max-width: 720px; margin: 0 auto; padding: 3rem 2rem; }\n"
    html += "    .post-hero { background: linear-gradient(135deg, #E0F7FC 0%, #B2EBF7 100%); border-radius: 16px; padding: 3rem 2rem; text-align: center; margin-bottom: 2rem; }\n"
    html += "    .post-emoji { font-size: 60px; margin-bottom: 1rem; }\n"
    html += "    .post-tag { font-size: 12px; background: #4DC8E8; color: #fff; padding: 4px 14px; border-radius: 99px; display: inline-block; margin-bottom: 1rem; }\n"
    html += "    .post-hero h1 { font-family: 'Noto Serif JP', serif; font-size: 24px; color: #1DA8CC; line-height: 1.5; margin-bottom: 0.5rem; }\n"
    html += "    .post-date { font-size: 13px; color: #1DA8CC; }\n"
    html += "    .post-content { background: #fff; border: 1px solid #B2EBF7; border-radius: 12px; padding: 2rem; line-height: 1.9; font-size: 15px; color: #333; }\n"
    html += "    .post-content h2 { font-size: 18px; font-weight: 700; color: #1DA8CC; margin: 2rem 0 1rem; padding-left: 0.8rem; border-left: 3px solid #4DC8E8; }\n"
    html += "    .post-content h3 { font-size: 16px; font-weight: 700; color: #4DC8E8; margin: 1.5rem 0 0.8rem; }\n"
    html += "    .post-content p { margin-bottom: 1rem; }\n"
    html += "    .post-content ul { padding-left: 1.5rem; margin-bottom: 1rem; }\n"
    html += "    .post-content li { margin-bottom: 0.4rem; }\n"
    html += "    .back-link { display: inline-block; margin-top: 2rem; color: #4DC8E8; text-decoration: none; font-size: 14px; }\n"
    html += "    .fixed-banner { position: fixed; bottom: 0; left: 0; right: 0; background: #1DA8CC; border-top: 1px solid rgba(255,255,255,0.1); padding: 12px 2rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; z-index: 300; }\n"
    html += "    .banner-text strong { font-size: 14px; color: #fff; display: block; }\n"
    html += "    .banner-text span { font-size: 11px; color: rgba(255,255,255,0.8); }\n"
    html += "    .banner-btn { background: #F8BBD9; color: #1DA8CC; border: none; border-radius: 6px; padding: 10px 20px; font-size: 13px; font-weight: 700; cursor: pointer; white-space: nowrap; text-decoration: none; }\n"
    html += "    footer { background: #1DA8CC; padding: 2rem; text-align: center; margin-top: 3rem; }\n"
    html += "    footer p { font-size: 13px; color: #fff; }\n"
    html += "  </style>\n"
    html += "</head>\n"
    html += "<body>\n"
    html += "<nav>\n"
    html += "  <a href=\"index.html\" class=\"nav-logo\">学習塾スタイル<span>JUKU STYLE</span></a>\n"
    html += "  <a href=\"members.html\" class=\"nav-btn\">生徒・保護者ログイン</a>\n"
    html += "</nav>\n"
    html += "<div class=\"post-container\">\n"
    html += "  <div class=\"post-hero\">\n"
    html += "    <div class=\"post-emoji\">" + emoji + "</div>\n"
    html += "    <span class=\"post-tag\">" + ptag + "</span>\n"
    html += "    <h1>" + ptitle + "</h1>\n"
    html += "    <p class=\"post-date\">" + pdate + "</p>\n"
    html += "  </div>\n"
    html += "  <div class=\"post-content\">" + pcontent + "</div>\n"
    html += "  <a href=\"blog.html\" class=\"back-link\">← ブログ一覧に戻る</a>\n"
    html += "</div>\n"
    html += "<div class=\"fixed-banner\">\n"
    html += "  <div class=\"banner-text\">\n"
    html += "    <strong>🎓体験授業 受付中！</strong>\n"
    html += "    <span>まずはお気軽にお問い合わせください</span>\n"
    html += "  </div>\n"
    html += "  <a href=\"index.html\" class=\"banner-btn\">入塾の流れを見る</a>\n"
    html += "</div>\n"
    html += "<footer>\n"
    html += "  <p>© 2025 学習塾スタイル</p>\n"
    html += "</footer>\n"
    html += "</body>\n"
    html += "</html>"
    
    with open("post_" + pid + ".html", "w", encoding="utf-8") as f:
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
    
    print("記事を生成しました：" + new_post['title'])

if __name__ == "__main__":
    main()
