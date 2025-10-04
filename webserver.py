import os
import requests
from flask import Flask, request, abort, render_template_string

app = Flask(__name__)
JSON_URL = "https://raw.githubusercontent.com/professerXisonCRACK/nenenen/main/cousins.json"

@app.route("/cousin/<user_id>", methods=["GET", "POST"])
def cousin_profile(user_id):
    # Fetch latest JSON from GitHub for live updates
    try:
        resp = requests.get(JSON_URL)
        resp.raise_for_status()
        cousins = resp.json()
    except Exception as e:
        return f"❌ Could not load data: {e}", 500

    data = cousins.get(user_id)
    if not data:
        return abort(404)

    if request.method == "POST":
        password = request.form.get("password")
        if password == data.get("password"):
            # Password correct → show profile page
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>{data['name']}'s Profile</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body {{
                        background-color: #ffffff;
                        color: #000000;
                        font-family: 'Segoe UI', sans-serif;
                    }}
                    .card {{
                        background-color: #f8f9fa;
                        border: none;
                        border-radius: 1rem;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                        transition: transform 0.3s, box-shadow 0.3s;
                        max-width: 600px;
                        margin: 50px auto;
                        text-align: center;
                    }}
                    .card:hover {{
                        transform: translateY(-8px);
                        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                    }}
                    .avatar {{
                        width: 120px;
                        height: 120px;
                        border-radius: 50%;
                        margin-top: -60px;
                        border: 5px solid #fff;
                    }}
                    .banner {{
                        width: 100%;
                        border-top-left-radius: 1rem;
                        border-top-right-radius: 1rem;
                        max-height: 200px;
                        object-fit: cover;
                        transition: transform 0.5s ease;
                    }}
                    .banner:hover {{
                        transform: scale(1.05);
                    }}
                    h1 {{
                        margin-top: 20px;
                        font-size: 2rem;
                    }}
                    p {{
                        font-size: 1.2rem;
                        margin: 5px 0;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    {"<img src='"+data.get('banner', '')+"' class='banner'>" if data.get('banner') else ""}
                    {"<img src='"+data.get('avatar', '')+"' class='avatar'>" if data.get('avatar') else ""}
                    <h1>{data['name']}</h1>
                    <p>🆔 Cousin ID: <strong>{data['cousin_id']}</strong></p>
                    <p>🏅 Rank: <strong>#{data['rank']}</strong></p>
                    <p>👀 Reputation: <strong>{data['rep']}/100</strong></p>
                </div>
            </body>
            </html>
            """
            return html
        else:
            return render_template_string("""
                <h1>❌ Wrong password!</h1>
                <a href="">Try again</a>
            """)

    # GET request → show password form
    return render_template_string("""
        <h1>Enter your password to view profile</h1>
        <form method="post">
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Submit</button>
        </form>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
