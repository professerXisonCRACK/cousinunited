import os
import requests
from flask import Flask, request, abort

app = Flask(__name__)
JSON_URL = "https://raw.githubusercontent.com/professerXisonCRACK/nenenen/refs/heads/main/cousins.json"

@app.route("/cousin/<user_id>")
def cousin_profile(user_id):
    token = request.args.get("token")

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
                background-color: #121212;
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
            }}
            .card {{
                background-color: #1e1e1e;
                border: none;
                border-radius: 1rem;
                box-shadow: 0 4px 20px rgba(0,0,0,0.6);
                transition: transform 0.3s, box-shadow 0.3s;
            }}
            .card:hover {{
                transform: translateY(-8px);
                box-shadow: 0 10px 40px rgba(0,0,0,0.8);
            }}
            .banner {{
                width: 100%;
                border-top-left-radius: 1rem;
                border-top-right-radius: 1rem;
                max-height: 300px;
                object-fit: cover;
                transition: transform 0.5s ease;
            }}
            .banner:hover {{
                transform: scale(1.05);
            }}
            .card-body p {{
                transition: color 0.3s;
            }}
            .card-body p:hover {{
                color: #00ffea;
            }}
            h1 {{
                margin-bottom: 0.5rem;
            }}
        </style>
    </head>
    <body>
        <div class="container my-5">
            <div class="card mx-auto" style="max-width: 600px;">
                {"<img src='"+data['banner']+"' class='banner'>" if data.get('banner') else ""}
                <div class="card-body text-center">
                    <h1 class="card-title">{data['name']}</h1>
                    <p class="card-text">🆔 <strong>{data['cousin_id']}</strong></p>
                    <p class="card-text">🏅 Rank: <strong>#{data['rank']}</strong></p>
                    <p class="card-text">👀 Reputation: <strong>{data['rep']}/100</strong></p>
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
