import os
import requests
from flask import Flask, request, abort

app = Flask(__name__)

# GitHub raw JSON URL
JSON_URL = "https://raw.githubusercontent.com/professerXisonCRACK/nenenen/main/cousins.json"

@app.route("/cousin/<user_id>")
def cousin_profile(user_id):
    token = request.args.get("token")
    if not token:
        return "❌ Token required in URL as ?token=...", 400

    # Fetch latest JSON from GitHub
    try:
        resp = requests.get(JSON_URL)
        resp.raise_for_status()
        cousins = resp.json()
    except Exception as e:
        return f"❌ Could not load data: {e}", 500

    data = cousins.get(user_id)
    if not data or data.get("token") != token:
        return abort(403)

    avatar_url = data.get("avatar", "")
    banner_url = data.get("banner", "")

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
            }}
            .card:hover {{
                transform: translateY(-8px);
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            }}
            .banner {{
                width: 100%;
                border-top-left-radius: 1rem;
                border-top-right-radius: 1rem;
                max-height: 300px;
                object-fit: cover;
            }}
            .avatar {{
                width: 120px;
                height: 120px;
                border-radius: 50%;
                object-fit: cover;
                margin-top: -60px;
                border: 5px solid white;
            }}
            h1 {{
                margin-top: 1rem;
                font-size: 2.5rem;
            }}
            p {{
                font-size: 1.2rem;
            }}
        </style>
    </head>
    <body>
        <div class="container my-5">
            <div class="card mx-auto" style="max-width: 600px; text-align: center;">
                {"<img src='"+banner_url+"' class='banner'>" if banner_url else ""}
                <img src="{avatar_url}" class="avatar">
                <div class="card-body">
                    <h1>{data['name']}</h1>
                    <p>🆔 <strong>{data['cousin_id']}</strong></p>
                    <p>🏅 Rank: <strong>#{data['rank']}</strong></p>
                    <p>👀 Reputation: <strong>{data['rep']}/100</strong></p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
