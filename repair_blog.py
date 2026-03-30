"""
repair_blog.py
blog_posts.json から blog.html を正しい状態に修復するスクリプト。
一度だけ実行してください。
"""
import json
import re
import os

EMOJIS = ["✏️", "💬", "📚", "🌟", "🎯", "🎮", "🌈", "🎵"]

def rebuild_blog_html(posts):
    cards_html = ""
    for i, post in enumerate(posts):
        emoji = EMOJIS[i % len(EMOJIS)]
        pid   = post['id']
        ptag  = post['tag']
        pdate = post['date']
        ptitle   = post['title']
        psummary = post['summary']
        cards_html += (
            f'\n    <a href="post_{pid}.html" class="blog-card">'
            f'\n      <div class="blog-img">{emoji}</div>'
            f'\n      <div class="blog-body">'
            f'\n        <div class="blog-meta">'
            f'\n          <span class="blog-tag">{ptag}</span>'
            f'\n          <span class="blog-date">{pdate}</span>'
            f'\n        </div>'
            f'\n        <h2>{ptitle}</h2>'
            f'\n        <p>{psummary}</p>'
            f'\n      </div>'
            f'\n    </a>'
        )

    new_grid = '<div class="blog-grid" id="blog-list">' + cards_html + "\n  </div>"

    with open("blog.html", "r", encoding="utf-8") as f:
        html = f.read()

    # blog-grid ブロック全体（内部の入れ子タグを含む）を正規表現で丸ごと置換
    html = re.sub(
        r'<div class="blog-grid" id="blog-list">.*?</div>(?=\s*</div>)',
        new_grid,
        html,
        flags=re.DOTALL
    )

    with open("blog.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ blog.html を {len(posts)} 記事で再構築しました。")

def main():
    if not os.path.exists("blog_posts.json"):
        print("❌ blog_posts.json が見つかりません。")
        return
    if not os.path.exists("blog.html"):
        print("❌ blog.html が見つかりません。")
        return

    with open("blog_posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)

    print(f"blog_posts.json から {len(posts)} 記事を読み込みました。")
    rebuild_blog_html(posts)

if __name__ == "__main__":
    main()
