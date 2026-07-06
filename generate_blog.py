import anthropic
import json
import os
import re
from datetime import datetime

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

EMOJIS = ["✏️", "💬", "📚", "🌟", "🎯", "🎮", "🌈", "🎵"]

def generate_blog_post(past_posts=None):
    today = datetime.now().strftime("%Y年%m月%d日")
    
    # 過去記事のタイトル一覧をプロンプト用に整形
    past_titles_block = ""
    if past_posts and len(past_posts) > 0:
        past_titles_block = "\n【過去に公開済みの記事タイトル一覧（重要）】\n"
        past_titles_block += "以下は当ブログで既に公開している記事です。テーマや切り口が重複しないよう、必ず違う内容の記事を書いてください。\n"
        past_titles_block += "同じ大テーマ（例：テスト効果、分散学習など）を扱う場合でも、具体例・実践方法・切り口を大きく変えてください。\n"
        for post in past_posts[:20]:  # 直近20件まで
            title = post.get('title', '')
            if title:
                past_titles_block += "・" + title + "\n"
        past_titles_block += "\n上記と重複しないテーマを選んでください。\n"
    
    prompt = """あなたは学習塾のプロ講師兼、教育・認知科学に詳しいライターです。
以下の条件でブログ記事を1つ作成してください。

【目的】
・勉強に役立つ理論・研究結果を、保護者や生徒にわかりやすく紹介する
・「なぜその勉強法が効くのか」を科学的根拠とともに伝える
・読んだ人が今日から実践できるヒントを持ち帰れる
・最終的に塾への信頼感を高める

【対象読者】
・小学生〜中学生の保護者
・勉強法を改善したい生徒本人

【テーマの選び方】
以下のような幅広い分野からテーマを選んでください。毎回異なる分野・切り口を意識すること。

■記憶と学習の科学
・分散学習（Spacing Effect）
・テスト効果（Testing Effect / Retrieval Practice）
・インターリービング（交互学習）
・精緻化（Elaboration）
・二重符号化（Dual Coding：文字と図の併用）
・生成効果（Generation Effect）
・忘却曲線（Ebbinghaus）

■モチベーションと意欲
・成長マインドセット（Growth Mindset）
・内発的動機付け vs 外発的動機付け
・自己決定理論（SDT）
・目標設定理論
・フロー状態
・自己効力感（Self-efficacy）

■認知能力・脳のはたらき
・ワーキングメモリの働きと鍛え方
・メタ認知（自分の理解度を客観視する力）
・注意と集中のメカニズム
・実行機能（Executive Function）
・脳の可塑性

■生活習慣と学習
・睡眠と記憶の関係
・運動と学習効果
・栄養・食事と認知能力
・スクリーンタイム（スマホ）の影響
・朝型 vs 夜型と学習効率

■学習環境と心理
・学習環境（音、照明、温度、片付け）
・テスト不安・プレッシャーへの対処
・ピア効果（一緒に学ぶ仲間の影響）
・ピグマリオン効果（期待の影響）
・ステレオタイプ脅威

■時間管理・習慣化
・ポモドーロ・テクニックの科学
・習慣形成のメカニズム
・スケジューリングと計画立て
・先延ばし行動（Procrastination）の心理学

【記事構成】
① 導入：保護者や生徒が抱きがちな疑問や思い込みを提示（150〜200文字）
② 紹介する理論・研究の概要をわかりやすく説明
③ 研究の具体例（誰がいつ行った研究か、結果がどうだったか）
④ なぜその結果になるのか、メカニズムの説明
⑤ 家庭や勉強での具体的な実践方法（あるあるレベルの具体例で）
⑥ よくある誤解や注意点
⑦ まとめ（今日から試せる一歩）
・H2見出しを4〜6個使って構成する

【トーン】
・知的で誠実、でも堅すぎない
・「先生が噛み砕いて教えてくれる」ような親しみやすさ
・断定しすぎず、「研究ではこう示されています」という丁寧な表現
・上から目線にならない
・適度にユーモアを混ぜてもよい（軽くクスッとする程度）

【必須条件】
・研究や理論を紹介する場合は、可能な範囲で研究者名・年代・研究内容に触れる
・専門用語は必ず日本語でかみくだいて説明する
・「なぜそうなるのか」のメカニズムを必ず説明する
・抽象論で終わらず、家庭や勉強机での具体的な実践方法に落とし込む
・1文は長くしすぎない
・箇条書きを適度に使う

【SEO強化】
・検索されやすいキーワード（例：「効率の良い勉強法」「記憶の定着」「集中力」など）を自然に含める
・見出しにもキーワードを入れる

【塾集客要素】
・最後に軽く塾の価値を伝える一文を入れる（押し売りにならない自然な形）
・例：「塾では、こうした研究をもとに指導法を設計しています」など

【禁止事項】
・存在しない研究や架空の研究者名をでっち上げる
  →自信がない場合は「ある研究では」「学習科学の分野では」とぼかす
・根拠のない断定
・精神論だけの内容
・薄い一般論
・お堅い教科書のような無機質な文章
・AIが書いたとわかるような硬い表現
・「**」（アスタリスク2つ）による強調記号を使わない。強調したい場合は<strong>タグを使う

【文字数】2000文字程度
""" + past_titles_block + """
今日の日付：""" + today + """

以下のJSON形式のみで返答してください（前後の説明文・```は不要）：
{
  "title": "SEOを意識した記事タイトル（30文字以内）",
  "tag": "カテゴリ（勉強法／受験対策／保護者向け／学習習慣／モチベーション のいずれか）",
  "summary": "記事の要約（80文字以内）",
  "content": "記事本文（2000文字程度、HTML可、見出しは<h2>タグを使用）"
}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
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
    
    # 正規表現でblog-gridブロック全体（入れ子のタグを含む）を正確に置換する
    html = re.sub(
        r'<div class="blog-grid" id="blog-list">.*?</div>(?=\s*</div>)',
        new_grid,
        html,
        flags=re.DOTALL
    )
    
    with open("blog.html", "w", encoding="utf-8") as f:
        f.write(html)

    # index.html のブログタブも同様に更新する
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            index_html = f.read()

        index_html = re.sub(
            r'<div class="blog-grid" id="blog-list">.*?</div>(?=\s*</div>)',
            new_grid,
            index_html,
            flags=re.DOTALL
        )

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(index_html)

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
    
    posts = load_blog_posts()
    post_data = generate_blog_post(past_posts=posts)
    
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
