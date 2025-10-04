import os
from flask import Flask, request, abort
import json

app = Flask(__name__)
DATA_FILE = "cousins.json"

@app.route("/cousin/<user_id>")
def cousin_profile(user_id):
    token = request.args.get("token")

    # Load fresh JSON each request for instant updates
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            cousins = json.load(f)
    else:
        cousins = {}

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
                background-color: #ffffff;
                color: #000000;
                font-family: 'Segoe UI', sans-serif;
            }}
            .card {{
                background-color: #f0f0f0;
                border-radius: 1rem;
                box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                transition: transform 0.3s, box-shadow 0.3s;
                padding: 2rem;
            }}
            .card:hover {{
                transform: translateY(-8px);
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            }}
            .avatar {{
                width: 120px;
                height: 120px;
                border-radius: 50%;
                margin: 0 auto 1rem auto;
                display: block;
            }}
            h1 {{
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }}
            p {{
                font-size: 1.2rem;
            }}
        </style>
    </head>
    <body>
        <div class="container my-5">
            <div class="card mx-auto text-center" style="max-width: 600px;">
                {"<img src='"+data['avatar']+"' class='avatar'>" if data.get('avatar') else ""}
                <h1>{data['name']}</h1>
                <p>🆔 <strong>{data['cousin_id']}</strong></p>
                <p>🏅 Rank: <strong>#{data['rank']}</strong></p>
                <p>👀 Reputation: <strong>{data['rep']}/100</strong></p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
